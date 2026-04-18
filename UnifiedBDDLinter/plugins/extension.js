/**
 * VS Code Extension for Unified BDD Linter
 * Provides real-time Gherkin file validation
 */

const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');


class UnifiedLinterExtension {
    constructor() {
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('unified-bdd-linter');
        this.linterPath = null;
        this.configuration = vscode.workspace.getConfiguration('unified-bdd-linter');
    }

    activate(context) {
        console.log('Unified BDD Linter activated');

        // Find linter.py path
        this.linterPath = this.findLinterPath();

        // Register commands
        context.subscriptions.push(
            vscode.commands.registerCommand('unified-bdd-linter.lint', () => this.lintCurrentFile()),
            vscode.commands.registerCommand('unified-bdd-linter.autofix', () => this.autoFixCurrentFile()),
            vscode.commands.registerCommand('unified-bdd-linter.lintFolder', (uri) => this.lintFolder(uri))
        );

        // Register event listeners
        context.subscriptions.push(
            vscode.workspace.onDidSaveTextDocument((doc) => {
                if (this.isFeatureFile(doc.fileName) && this.configuration.get('autoLintOnSave')) {
                    this.lintFile(doc.fileName);
                }
            }),
            vscode.workspace.onDidOpenTextDocument((doc) => {
                if (this.isFeatureFile(doc.fileName)) {
                    this.lintFile(doc.fileName);
                }
            })
        );

        // Initial lint of open files
        vscode.workspace.textDocuments.forEach(doc => {
            if (this.isFeatureFile(doc.fileName)) {
                this.lintFile(doc.fileName);
            }
        });
    }

    findLinterPath() {
        const configPath = this.configuration.get('linterPath');
        if (configPath && fs.existsSync(configPath)) {
            return configPath;
        }

        // Search for linter.py in workspace
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (workspaceFolders) {
            for (const folder of workspaceFolders) {
                const linterPath = path.join(folder.uri.fsPath, 'linter.py');
                if (fs.existsSync(linterPath)) {
                    return linterPath;
                }
            }
        }

        return null;
    }

    isFeatureFile(fileName) {
        return fileName.endsWith('.feature');
    }

    lintFile(fileName) {
        if (!this.linterPath) {
            vscode.window.showErrorMessage('Unified BDD Linter: linter.py not found');
            return;
        }

        const python = 'python3';
        const args = [this.linterPath, fileName, '--format', 'json'];

        const process = spawn(python, args);
        let stdout = '';
        let stderr = '';

        process.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        process.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        process.on('close', (code) => {
            this.parseLintOutput(fileName, stdout, stderr);
        });
    }

    parseLintOutput(fileName, stdout, stderr) {
        try {
            const output = JSON.parse(stdout);
            const diagnostics = [];

            if (output.files && output.files[fileName]) {
                const violations = output.files[fileName];

                violations.forEach(violation => {
                    const line = Math.max(0, violation.line - 1);
                    const column = Math.max(0, violation.column - 1);

                    const range = new vscode.Range(
                        new vscode.Position(line, column),
                        new vscode.Position(line, column + 10)
                    );

                    const severity = this.getSeverity(violation.severity);
                    const message = `[${violation.rule}] ${violation.message}`;

                    const diagnostic = new vscode.Diagnostic(range, message, severity);
                    diagnostic.code = violation.rule;
                    diagnostic.source = 'Unified BDD Linter';

                    if (violation.suggestion) {
                        diagnostic.relatedInformation = [
                            new vscode.DiagnosticRelatedInformation(
                                new vscode.Location(vscode.Uri.file(fileName), range),
                                `Fix: ${violation.suggestion}`
                            )
                        ];
                    }

                    diagnostics.push(diagnostic);
                });

                this.diagnosticCollection.set(vscode.Uri.file(fileName), diagnostics);
            }
        } catch (error) {
            console.error('Failed to parse linter output:', error);
        }
    }

    getSeverity(severity) {
        const severityMap = {
            'info': vscode.DiagnosticSeverity.Hint,
            'warning': vscode.DiagnosticSeverity.Warning,
            'error': vscode.DiagnosticSeverity.Error,
            'critical': vscode.DiagnosticSeverity.Error
        };
        return severityMap[severity] || vscode.DiagnosticSeverity.Warning;
    }

    lintCurrentFile() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No file is currently open');
            return;
        }

        if (!this.isFeatureFile(editor.document.fileName)) {
            vscode.window.showErrorMessage('Current file is not a Gherkin feature file');
            return;
        }

        this.lintFile(editor.document.fileName);
        vscode.window.showInformationMessage('Linting complete');
    }

    autoFixCurrentFile() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No file is currently open');
            return;
        }

        if (!this.isFeatureFile(editor.document.fileName)) {
            vscode.window.showErrorMessage('Current file is not a Gherkin feature file');
            return;
        }

        const autoFixPath = path.join(path.dirname(this.linterPath), 'auto_fix.py');
        const python = 'python3';
        const args = [autoFixPath, editor.document.fileName];

        const process = spawn(python, args);

        process.on('close', (code) => {
            if (code === 0) {
                editor.document.save().then(() => {
                    this.lintFile(editor.document.fileName);
                    vscode.window.showInformationMessage('Auto-fix complete');
                });
            } else {
                vscode.window.showErrorMessage('Auto-fix failed');
            }
        });
    }

    lintFolder(uri) {
        if (!uri) {
            vscode.window.showErrorMessage('No folder selected');
            return;
        }

        const folderPath = uri.fsPath;
        const python = 'python3';
        const args = [this.linterPath, folderPath, '--format', 'json'];

        const process = spawn(python, args);
        let stdout = '';

        process.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        process.on('close', (code) => {
            try {
                const output = JSON.parse(stdout);
                const totalViolations = output.summary.total_violations;
                const totalErrors = output.summary.total_errors;

                vscode.window.showInformationMessage(
                    `Linting complete: ${totalViolations} violations, ${totalErrors} errors`
                );
            } catch (error) {
                vscode.window.showErrorMessage('Failed to lint folder');
            }
        });
    }
}

function activate(context) {
    const extension = new UnifiedLinterExtension();
    extension.activate(context);
}

function deactivate() {
    console.log('Unified BDD Linter deactivated');
}

module.exports = {
    activate,
    deactivate
};
