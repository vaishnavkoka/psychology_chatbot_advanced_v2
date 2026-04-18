@REM Licensed to the Apache Software Foundation (ASF) under one
@REM or more contributor license agreements.  See the NOTICE file
@REM distributed with this work for additional information
@REM regarding copyright ownership.  The ASF licenses this file
@REM to you under the Apache License, Version 2.0 (the
@REM "License"); you may not use this file except in compliance
@REM with the License.  You may obtain a copy of the License at
@REM
@REM    https://www.apache.org/licenses/LICENSE-2.0
@REM
@REM Unless required by applicable law or agreed to in writing,
@REM software distributed under the License is distributed on an
@REM "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
@REM KIND, either express or implied.  See the License for the
@REM specific language governing permissions and limitations
@REM under the License.
@REM
@REM This batch file was originally developed by the Maven project
@REM (https://maven.apache.org)
@REM but is now maintained as part of the Maven Wrapper project
@REM (https://github.com/apache/maven-wrapper).
@REM
@REM Apache Maven Wrapper batch script
@REM Optional ENV vars
@REM   M2_HOME - location of maven2 to use (default searches %PATH% for mvn and use its parent dir)
@REM   MAVEN_SKIP_RC - flag to disable loading of mavenrc files
@REM Optional system properties
@REM   maven.home - M2_HOME root folder. If set, then the pure java implementation is used
@REM   maven.multiModuleProjectDirectory - root folder. If set, then the sources will be read from this folder
@REM
@REM See other scripts in bin folder for more details
@REM-----

@setlocal
@if not "%JAVA_HOME%" == "" goto OkJHome

for %%i in (java.exe) do set "JAVA_EXE=%%~$PATH:i"
if exist "%JAVA_EXE%" (
  set "JAVA_HOME=%%~dp1"
) else (
  echo Error: JAVA_HOME not found in your environment. >&2
  exit /b 1
)
goto endInit

:OkJHome
if exist "%JAVA_HOME%\bin\java.exe" (
  set "JAVA_EXE=%JAVA_HOME%\bin\java.exe"
) else (
  echo Error: JAVA_HOME is set to an invalid directory. >&2
  echo JAVA_HOME = "%JAVA_HOME%" >&2
  echo Please set the JAVA_HOME variable in your environment to match the >&2
  echo location of your Java installation. >&2
  exit /b 1
)

:endInit

set MAVEN_WRAPPER_JAR=%~dp0.mvn\wrapper\maven-wrapper.jar
if exist "%MAVEN_WRAPPER_JAR%" (
  "%JAVA_EXE%" -classpath "%MAVEN_WRAPPER_JAR%" "-Dmaven.home=%~dp0.mvn/wrapper" "-Dclassworlds.conf=%~dp0.mvn/wrapper/m2.conf" "org.apache.maven.wrapper.MavenWrapperMain" %*
) else (
  echo Error: Maven wrapper JAR not found. >&2
  exit /b 1
)
endlocal
