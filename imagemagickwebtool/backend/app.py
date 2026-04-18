"""
Image Mutation Tool - Flask Backend
Main application entry point with image processing mutations using ImageMagick
"""

import os
import json
import uuid
import zipfile
from io import BytesIO
from datetime import datetime
from flask import Flask, request, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from wand.image import Image as WandImage
from wand.color import Color
from PIL import Image as PILImage
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    
    # Configuration
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 52428800))  # 50MB
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    app.config['OUTPUT_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    
    # Enable CORS
    CORS(app)
    
    # ==================== PIL MUTATION HELPERS ====================
    
    def apply_pil_mutation(pil_image, mutation_name, **params):
        """Apply mutations to PIL images for formats Wand can't handle"""
        from PIL import ImageOps, ImageEnhance, ImageFilter, ImageDraw
        
        img = pil_image.copy()
        
        if mutation_name == 'grayscale':
            return ImageOps.grayscale(img)
        
        elif mutation_name == 'blur':
            sigma = float(params.get('sigma', 5))
            radius = sigma * 0.4
            return img.filter(ImageFilter.GaussianBlur(radius=radius))
        
        elif mutation_name == 'black_threshold':
            percentage = float(params.get('percentage', 25))
            threshold = int((percentage / 100.0) * 255)
            # Convert to grayscale, then apply threshold
            if img.mode != 'L':
                img_gray = ImageOps.grayscale(img)
            else:
                img_gray = img
            # Apply threshold
            img_threshold = ImageOps.autocontrast(img_gray)
            return img_threshold
        
        elif mutation_name == 'border':
            pixels = int(params.get('pixels', 10))
            border_color = params.get('color', (200, 200, 200))
            return ImageOps.expand(img, border=pixels, fill=border_color)
        
        elif mutation_name == 'charcoal':
            radius = float(params.get('radius', 5))
            # Create charcoal effect using edge detection + blur
            img_edge = img.filter(ImageFilter.FIND_EDGES)
            img_inv = ImageOps.invert(img_edge.convert('L'))
            return img_inv.convert('RGB')
        
        elif mutation_name == 'color_reduce':
            colors = int(params.get('colors', 8))
            if img.mode != 'P':
                img = img.quantize(colors=colors)
            return img
        
        elif mutation_name == 'colorize':
            tone = params.get('tone', 'blue').lower()
            gs = ImageOps.grayscale(img)
            gs_rgb = gs.convert('RGB')
            
            # Tone color mappings
            tone_colors = {
                'red': (255, 100, 100),
                'green': (100, 255, 100),
                'blue': (100, 100, 255),
                'yellow': (255, 255, 100),
                'cyan': (100, 255, 255),
                'magenta': (255, 100, 255),
                'sepia': (112, 66, 20)
            }
            
            tone_color = tone_colors.get(tone, (100, 100, 255))
            
            # Create colored overlay
            overlay = PILImage.new('RGB', img.size, tone_color)
            return PILImage.blend(gs_rgb, overlay, 0.4)
        
        elif mutation_name == 'colorspace':
            colorspace = params.get('colorspace', 'RGB').upper()
            if colorspace == 'GRAY':
                return ImageOps.grayscale(img)
            elif colorspace == 'HSV':
                # Convert to HSV (PIL doesn't support directly, use RGB)
                return img.convert('RGB')
            elif colorspace == 'LAB':
                # LAB conversion is complex, approximate with grayscale
                return ImageOps.grayscale(img)
            else:
                return img.convert('RGB')
        
        elif mutation_name == 'annotate':
            text = params.get('text', 'Watermark').strip()
            if not text:
                return img
            position = params.get('position', 'center')
            font_size = int(params.get('fontSize', 36))
            
            from PIL import ImageFont
            canvas = img.copy()
            draw = ImageDraw.Draw(canvas)
            
            # Try to use default font, fallback to default
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            img_width, img_height = canvas.size
            
            positions = {
                'center': ((img_width - text_width) // 2, (img_height - text_height) // 2),
                'northwest': (10, 10),
                'north': ((img_width - text_width) // 2, 10),
                'northeast': (img_width - text_width - 10, 10),
                'west': (10, (img_height - text_height) // 2),
                'east': (img_width - text_width - 10, (img_height - text_height) // 2),
                'southwest': (10, img_height - text_height - 10),
                'south': ((img_width - text_width) // 2, img_height - text_height - 10),
                'southeast': (img_width - text_width - 10, img_height - text_height - 10)
            }
            
            pos = positions.get(position, (10, 10))
            
            # Draw text with white color and black outline
            outline_range = 2
            for adj_x in range(-outline_range, outline_range + 1):
                for adj_y in range(-outline_range, outline_range + 1):
                    draw.text((pos[0] + adj_x, pos[1] + adj_y), text, font=font, fill=(0, 0, 0))
            draw.text(pos, text, font=font, fill=(255, 255, 255))
            
            return canvas
        
        elif mutation_name == 'chop':
            chop_type = params.get('type', 'horizontal')
            pixels = int(params.get('value', 50))
            
            width, height = img.size
            
            if chop_type == 'horizontal':
                # Remove from left and right
                return img.crop((pixels, 0, width - pixels, height))
            elif chop_type == 'vertical':
                # Remove from top and bottom
                return img.crop((0, pixels, width, height - pixels))
            elif chop_type == 'center':
                # Crop from center
                left = pixels
                top = pixels
                right = width - pixels
                bottom = height - pixels
                return img.crop((left, top, right, bottom))
            else:
                return img
        
        elif mutation_name == 'brightness':
            percentage = float(params.get('percentage', 50))
            factor = (100 + percentage) / 100.0
            enhancer = ImageEnhance.Brightness(img)
            return enhancer.enhance(factor)
        
        elif mutation_name == 'rotation':
            degrees = float(params.get('degrees', 15))
            return img.rotate(degrees, expand=False, fillcolor='white')
        
        elif mutation_name == 'contrast':
            percentage = float(params.get('percentage', 50))
            factor = (100 + percentage) / 100.0
            enhancer = ImageEnhance.Contrast(img)
            return enhancer.enhance(factor)
        
        elif mutation_name == 'saturation':
            percentage = float(params.get('percentage', 50))
            factor = (100 + percentage) / 100.0
            enhancer = ImageEnhance.Color(img)
            return enhancer.enhance(factor)
        
        else:
            return img
    
    # ==================== MUTATION IMPLEMENTATIONS ====================
    
    class ImageMutator:
        """Image mutation processor using ImageMagick"""
        
        @staticmethod
        def blur(image, sigma=5):
            """Apply Gaussian blur using ImageMagick"""
            sigma = float(sigma)
            image.blur(radius=sigma*0.4, sigma=sigma)
            return image
        
        @staticmethod
        def black_threshold(image, percentage=25):
            """Apply black threshold to image"""
            percentage = float(percentage)
            threshold = int((percentage / 100.0) * 65535)  # Wand uses 0-65535 range
            image.black_threshold(threshold=threshold)
            return image
        
        @staticmethod
        def border(image, pixels=10):
            """Add colored border to image"""
            pixels = int(pixels)
            image.border(width=pixels, height=pixels, color=Color('gray(200)'))
            return image
        
        @staticmethod
        def charcoal(image, radius=5):
            """Apply charcoal sketch effect"""
            radius = float(radius)
            # Wand charcoal requires both radius and sigma parameters
            # sigma controls the blur effect (higher = more blur)
            sigma = radius * 0.5  # Proportional sigma based on radius
            image.charcoal(radius=radius, sigma=sigma)
            return image
        
        @staticmethod
        def brightness(image, percentage=0):
            """Adjust brightness using ImageMagick"""
            percentage = float(percentage)
            # Convert percentage to brightness multiplier (0-200%)
            factor = 100 + percentage  # ranges from 0 to 200
            image.brightness = factor
            return image
        
        @staticmethod
        def rotation(image, degrees=15):
            """Rotate image using ImageMagick"""
            angle = float(degrees)
            image.rotate(-angle)
            return image
        
        @staticmethod
        def contrast(image, percentage=0):
            """Adjust contrast using ImageMagick"""
            percentage = float(percentage)
            # Convert percentage to contrast adjustment
            factor = 100 + percentage
            image.contrast = factor
            return image
        
        @staticmethod
        def saturation(image, percentage=0):
            """Adjust color saturation using ImageMagick"""
            percentage = float(percentage)
            # Convert percentage to saturation multiplier
            factor = 100 + percentage
            image.modulate(saturation=factor)
            return image
        
        @staticmethod
        def color_reduce(image, colors=8):
            """Reduce color palette using ImageMagick quantization"""
            num_colors = int(colors)
            # Quantize to specified number of colors
            image.quantize(number_colors=num_colors)
            return image
        
        @staticmethod
        def colorize(image, tone='blue'):
            """Apply color tint using ImageMagick"""
            tone = str(tone).lower()
            
            if tone == 'grayscale':
                image.colorspace = 'gray'
            else:
                # Apply color tint by modulating hue and saturation
                hue_shifts = {
                    'red': 0,
                    'green': 120,
                    'blue': 240,
                    'yellow': -60,
                    'cyan': 180,
                    'magenta': 300,
                    'sepia': -30
                }
                hue = hue_shifts.get(tone, 0)
                # Modulate is modulation(brightness, saturation, hue)
                image.modulate(brightness=100, saturation=150, hue=hue)
            
            return image
        
        @staticmethod
        def colorspace(image, colorspace='RGB'):
            """Convert to different colorspace"""
            colorspace = str(colorspace).upper()
            if colorspace == 'GRAY':
                image.colorspace = 'gray'
            elif colorspace == 'HSV':
                image.colorspace = 'hsv'
            elif colorspace == 'HCL':
                image.colorspace = 'hcl'
            elif colorspace == 'CMY':
                image.colorspace = 'cmy'
            elif colorspace == 'CMYK':
                image.colorspace = 'cmyk'
            elif colorspace == 'YCBCR':
                image.colorspace = 'ycbcr'
            elif colorspace == 'LAB':
                image.colorspace = 'lab'
            else:
                image.colorspace = 'rgb'
            
            return image
        
        @staticmethod
        def annotate(image, text='Watermark', position='center', fontSize='36'):
            """Add text annotation to image"""
            from wand.drawing import Drawing
            from wand.display import display
            
            text_str = str(text)[:100]
            font_size = int(fontSize)
            
            with Drawing() as draw:
                draw.font_size = font_size
                draw.fill_color = Color('white')
                draw.stroke_color = Color('black')
                draw.stroke_width = 2
                
                # Calculate text metrics
                metrics = draw.get_font_metrics(image, text_str)
                text_width = metrics[4] - metrics[0]
                text_height = metrics[5] - metrics[1]
                
                img_width = image.width
                img_height = image.height
                
                # Position mappings
                positions = {
                    'center': ((img_width - text_width) / 2, (img_height - text_height) / 2),
                    'northwest': (10, 20),
                    'north': ((img_width - text_width) / 2, 20),
                    'northeast': (img_width - text_width - 10, 20),
                    'west': (10, (img_height - text_height) / 2),
                    'east': (img_width - text_width - 10, (img_height - text_height) / 2),
                    'southwest': (10, img_height - text_height - 10),
                    'south': ((img_width - text_width) / 2, img_height - text_height - 10),
                    'southeast': (img_width - text_width - 10, img_height - text_height - 10)
                }
                
                x, y = positions.get(position, (10, 20))
                draw.text(int(x), int(y), text_str)
                draw(image)
            
            return image
        
        @staticmethod
        def chop(image, type='horizontal', value=50):
            """Crop/chop parts of the image"""
            pixels = int(value)
            img_width = image.width
            img_height = image.height
            
            if type == 'horizontal':
                # Chop from left and right
                image.crop(left=pixels, top=0, right=img_width - pixels, bottom=img_height)
            elif type == 'vertical':
                # Chop from top and bottom
                image.crop(left=0, top=pixels, right=img_width, bottom=img_height - pixels)
            elif type == 'center':
                # Chop from center
                image.crop(left=pixels, top=pixels, right=img_width - pixels, bottom=img_height - pixels)
            
            return image
        
        @staticmethod
        def grayscale(image, **kwargs):
            """Convert to grayscale using ImageMagick"""
            image.colorspace = 'gray'
            return image
    
    # ==================== API ENDPOINTS ====================
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'version': '1.0.0',
            'message': 'Image Mutation Tool API is running'
        }, 200
    
    @app.route('/api/mutations', methods=['GET'])
    def get_mutations():
        """Get all available mutations"""
        mutations = {
            'continuous': {
                'blur': {
                    'name': 'Blur (Gaussian)',
                    'description': 'Apply Gaussian blur effect to soften image',
                    'category': 'continuous',
                    'parameters': {
                        'sigma': {
                            'type': 'float',
                            'min': 0.1,
                            'max': 20,
                            'step': 0.5,
                            'default': 5,
                            'description': 'Blur strength - 0.1=sharp, 20=extreme blur'
                        }
                    }
                },
                'black_threshold': {
                    'name': 'Black Threshold',
                    'description': 'Convert pixels below threshold to black',
                    'category': 'continuous',
                    'parameters': {
                        'percentage': {
                            'type': 'int',
                            'min': 0,
                            'max': 100,
                            'step': 5,
                            'default': 25,
                            'description': 'Brightness threshold percentage'
                        }
                    }
                },
                'border': {
                    'name': 'Border',
                    'description': 'Add colored border around image',
                    'category': 'continuous',
                    'parameters': {
                        'pixels': {
                            'type': 'int',
                            'min': 0,
                            'max': 100,
                            'step': 5,
                            'default': 10,
                            'description': 'Border width in pixels'
                        }
                    }
                },
                'charcoal': {
                    'name': 'Charcoal Effect',
                    'description': 'Apply charcoal/sketch effect to image',
                    'category': 'continuous',
                    'parameters': {
                        'radius': {
                            'type': 'float',
                            'min': 0.2,
                            'max': 10,
                            'step': 0.2,
                            'default': 5,
                            'description': 'Sketch intensity - 0.2=subtle, 10=heavy'
                        }
                    }
                },
                'color_reduce': {
                    'name': 'Color Palette',
                    'description': 'Reduce number of colors in palette',
                    'category': 'continuous',
                    'parameters': {
                        'colors': {
                            'type': 'int',
                            'min': 2,
                            'max': 256,
                            'step': 1,
                            'default': 16,
                            'description': 'Number of colors - 2=B&W, 256=full'
                        }
                    }
                },
                'brightness': {
                    'name': 'Brightness',
                    'description': 'Adjust image brightness',
                    'category': 'continuous',
                    'parameters': {
                        'percentage': {
                            'type': 'int',
                            'min': -100,
                            'max': 100,
                            'step': 5,
                            'default': 0,
                            'description': 'Brightness adjustment (-100 to +100)'
                        }
                    }
                },
                'rotation': {
                    'name': 'Rotation',
                    'description': 'Rotate image by angle',
                    'category': 'continuous',
                    'parameters': {
                        'degrees': {
                            'type': 'float',
                            'min': 0,
                            'max': 360,
                            'step': 5,
                            'default': 0,
                            'description': 'Rotation angle in degrees'
                        }
                    }
                },
                'contrast': {
                    'name': 'Contrast',
                    'description': 'Adjust image contrast',
                    'category': 'continuous',
                    'parameters': {
                        'percentage': {
                            'type': 'int',
                            'min': -100,
                            'max': 100,
                            'step': 5,
                            'default': 0,
                            'description': 'Contrast adjustment percentage'
                        }
                    }
                },
                'saturation': {
                    'name': 'Saturation',
                    'description': 'Adjust color saturation',
                    'category': 'continuous',
                    'parameters': {
                        'percentage': {
                            'type': 'int',
                            'min': -100,
                            'max': 200,
                            'step': 10,
                            'default': 0,
                            'description': 'Saturation adjustment percentage'
                        }
                    }
                }
            },
            'discrete': {
                'colorize': {
                    'name': 'Colorize',
                    'description': 'Apply color tone to grayscale image',
                    'category': 'discrete',
                    'parameters': {
                        'tone': {
                            'type': 'choice',
                            'options': ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'sepia'],
                            'default': 'blue',
                            'description': 'Color tone to apply'
                        }
                    }
                },
                'colorspace': {
                    'name': 'Colorspace Conversion',
                    'description': 'Convert to different color model',
                    'category': 'discrete',
                    'parameters': {
                        'colorspace': {
                            'type': 'choice',
                            'options': ['RGB', 'Gray', 'HSV', 'HCL', 'CMY', 'CMYK', 'YCbCr', 'Lab'],
                            'default': 'RGB',
                            'description': 'Target color model'
                        }
                    }
                },
                'annotate': {
                    'name': 'Text Annotation',
                    'description': 'Add text watermark to image',
                    'category': 'discrete',
                    'parameters': {
                        'text': {
                            'type': 'string',
                            'max_length': 100,
                            'default': '',
                            'description': 'Text to add'
                        },
                        'position': {
                            'type': 'choice',
                            'options': ['center', 'northwest', 'north', 'northeast', 'west', 'east', 'southwest', 'south', 'southeast'],
                            'default': 'center',
                            'description': 'Text position'
                        },
                        'fontSize': {
                            'type': 'choice',
                            'options': ['24', '36', '48', '72'],
                            'default': '36',
                            'description': 'Font size'
                        }
                    }
                },
                'chop': {
                    'name': 'Chop/Crop',
                    'description': 'Crop parts of image',
                    'category': 'discrete',
                    'parameters': {
                        'type': {
                            'type': 'choice',
                            'options': ['horizontal', 'vertical', 'center'],
                            'default': 'horizontal',
                            'description': 'Crop direction'
                        },
                        'value': {
                            'type': 'int',
                            'min': 1,
                            'max': 200,
                            'default': 50,
                            'description': 'Pixels to remove'
                        }
                    }
                },
                'grayscale': {
                    'name': 'Grayscale',
                    'description': 'Convert image to grayscale',
                    'category': 'discrete',
                    'parameters': {}
                }
            }
        }
        
        return mutations, 200
    
    @app.route('/api/mutate', methods=['POST'])
    def mutate_image():
        """Apply mutation to image using ImageMagick via Wand"""
        try:
            # Check if files are in request
            if 'image' not in request.files:
                return {'error': 'No image file provided'}, 400
            
            file = request.files['image']
            if file.filename == '':
                return {'error': 'No file selected'}, 400
            
            # Get mutation and parameters
            mutation_name = request.form.get('mutation')
            params_str = request.form.get('parameters', '{}')
            
            if not mutation_name:
                return {'error': 'No mutation specified'}, 400
            
            # Parse parameters
            try:
                params = json.loads(params_str)
            except:
                params = {}
            
            # Extract original filename and extension
            original_filename = file.filename
            name_without_ext = os.path.splitext(original_filename)[0]
            file_ext = os.path.splitext(original_filename)[1].lower()
            
            # Map extensions to format names
            ext_to_format = {
                '.jpg': 'jpeg',
                '.jpeg': 'jpeg',
                '.png': 'png',
                '.gif': 'gif',
                '.webp': 'webp',
                '.bmp': 'bmp',
                '.tiff': 'tiff',
                '.tif': 'tiff'
            }
            
            # Determine output format (preserve original)
            original_format = ext_to_format.get(file_ext, 'jpeg')
            
            # Open image
            try:
                # Read file bytes
                file.seek(0)
                image_bytes = file.read()
                
                # Try to open directly with Wand first
                image = None
                use_pil = False
                try:
                    image = WandImage(blob=image_bytes)
                except Exception as wand_error:
                    # If Wand fails, fall back to PIL for the entire pipeline
                    logger.warning(f"Wand failed: {wand_error}, falling back to PIL")
                    use_pil = True
                
                if use_pil:
                    # Use PIL to open and validate
                    try:
                        pil_img = PILImage.open(BytesIO(image_bytes))
                        
                        # Store PIL image for later mutation
                        # We'll use PIL for mutations instead of Wand
                        image = pil_img
                        logger.info(f"Opened image with PIL: {pil_img.format} {pil_img.mode}")
                    except Exception as pil_error:
                        logger.error(f"PIL open failed: {pil_error}")
                        raise wand_error  # Raise the original Wand error
                        
            except Exception as e:
                return {'error': f'Invalid image file: {str(e)}'}, 400
            
            # Save original with unique ID, preserving format
            unique_id = str(uuid.uuid4())[:8]
            storage_original_filename = f"{unique_id}_original{file_ext}"
            original_path = os.path.join(app.config['OUTPUT_FOLDER'], storage_original_filename)
            
            if use_pil:
                # Save PIL image in original format
                pil_save_kwargs = {}
                if original_format == 'jpeg':
                    pil_save_kwargs['quality'] = 90
                image.save(original_path, format=original_format.upper() if original_format != 'tiff' else 'TIFF', **pil_save_kwargs)
            else:
                # Save Wand image
                image.format = original_format
                image.save(filename=original_path)
            
            # Apply mutation
            mutator = ImageMutator()
            mutation_func = getattr(mutator, mutation_name, None)
            
            if not mutation_func:
                return {'error': f'Unknown mutation: {mutation_name}'}, 400
            
            try:
                if use_pil:
                    # For PIL images, apply simple PIL-based mutations
                    mutated_image = apply_pil_mutation(image, mutation_name, **params)
                else:
                    # For Wand images, use the existing mutator
                    mutated_image = mutation_func(image, **params)
            except Exception as e:
                return {'error': f'Mutation failed: {str(e)}'}, 500
            
            # Save result with unique ID and mutation name, preserving format
            storage_result_filename = f"{unique_id}_result{file_ext}"
            result_path = os.path.join(app.config['OUTPUT_FOLDER'], storage_result_filename)
            
            # Save result
            if use_pil:
                # Save PIL image in original format
                pil_save_kwargs = {}
                if original_format == 'jpeg':
                    pil_save_kwargs['quality'] = 90
                mutated_image.save(result_path, format=original_format.upper() if original_format != 'tiff' else 'TIFF', **pil_save_kwargs)
            else:
                # Ensure Wand image has correct format
                if not mutated_image.format or mutated_image.format.lower() != original_format:
                    try:
                        mutated_image.format = original_format
                    except Exception as fmt_error:
                        logger.warning(f"Could not set format to {original_format}: {fmt_error}")
                
                # Set compression quality if JPEG
                if original_format == 'jpeg':
                    mutated_image.compression_quality = 90
                
                mutated_image.save(filename=result_path)
            
            # Create user-friendly download filename
            # Clean up filename - remove special characters
            safe_name = "".join(c for c in name_without_ext if c.isalnum() or c in ('-', '_', ' ')).strip()
            download_filename = f"{safe_name}_{mutation_name}{file_ext}"
            
            # Build absolute URLs for CORS compatibility
            base_url = request.url_root.rstrip('/')
            original_url = f'{base_url}/api/image/{storage_original_filename}'
            result_url = f'{base_url}/api/image/{storage_result_filename}'
            download_url = f'{base_url}/api/download/{storage_result_filename}?filename={download_filename}'
            
            # Return response with URLs and metadata
            return {
                'success': True,
                'mutation': mutation_name,
                'parameters': params,
                'original_filename': original_filename,
                'download_filename': download_filename,
                'original_url': original_url,
                'result_url': result_url,
                'download_url': download_url,
                'timestamp': datetime.now().isoformat()
            }, 200
        
        except Exception as e:
            logger.error(f"Mutation error: {str(e)}")
            return {'error': f'Server error: {str(e)}'}, 500
    
    @app.route('/api/image/<filename>', methods=['GET'])
    def get_image(filename):
        """Serve result images"""
        try:
            # Validate filename to prevent path traversal
            if '/' in filename or '\\' in filename:
                return {'error': 'Invalid filename'}, 400
            
            image_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            
            if not os.path.exists(image_path):
                return {'error': 'Image not found'}, 404
            
            return send_file(image_path, mimetype='image/jpeg')
        except Exception as e:
            return {'error': str(e)}, 500
    
    @app.route('/api/download/<filename>', methods=['GET'])
    def download_image(filename):
        """Download result image with custom filename"""
        try:
            # Validate filename
            if '/' in filename or '\\' in filename:
                return {'error': 'Invalid filename'}, 400
            
            image_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            
            if not os.path.exists(image_path):
                return {'error': 'Image not found'}, 404
            
            # Get custom download name from query parameter
            download_name = request.args.get('filename', filename)
            
            # Detect file format from filename
            file_ext = os.path.splitext(download_name)[1].lower()
            
            # Map extensions to MIME types
            mime_types = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp',
                '.bmp': 'image/bmp',
                '.tiff': 'image/tiff',
                '.tif': 'image/tiff'
            }
            
            mimetype = mime_types.get(file_ext, 'image/jpeg')
            
            # If filename doesn't have an extension, try to preserve original format
            if not file_ext:
                # Extract format from stored file
                _, stored_ext = os.path.splitext(filename)
                if stored_ext:
                    download_name += stored_ext
                    mimetype = mime_types.get(stored_ext.lower(), 'image/jpeg')
            
            # Return file with proper attachment header
            return send_file(
                image_path,
                mimetype=mimetype,
                as_attachment=True,
                download_name=download_name
            )
        except Exception as e:
            return {'error': str(e)}, 500
    
    @app.route('/api/download-batch', methods=['POST'])
    def download_batch():
        """Download multiple images as ZIP archive"""
        try:
            data = request.get_json()
            if not data or 'results' not in data:
                return {'error': 'No results provided'}, 400
            
            results = data['results']
            if not results:
                return {'error': 'Empty results'}, 400
            
            # Create ZIP in memory
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for result in results:
                    url = result.get('url', '')
                    filename = result.get('filename', 'image.jpg')
                    
                    # Extract file ID from URL (e.g., /api/image/uuid_result.jpg -> uuid_result.jpg)
                    if '/api/image/' in url:
                        file_id = url.split('/api/image/')[-1]
                        file_path = os.path.join(app.config['OUTPUT_FOLDER'], file_id)
                        
                        if os.path.exists(file_path):
                            # Read file and add to ZIP
                            with open(file_path, 'rb') as f:
                                zip_file.writestr(filename, f.read())
            
            # Prepare ZIP for download
            zip_buffer.seek(0)
            return send_file(
                zip_buffer,
                mimetype='application/zip',
                as_attachment=True,
                download_name=f'mutated_images_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
            )
        
        except Exception as e:
            logger.error(f"Batch download error: {str(e)}")
            return {'error': f'Batch download failed: {str(e)}'}, 500
    
    return app

# Create the app
app = create_app()

if __name__ == '__main__':
    debug = os.getenv('DEBUG', 'False') == 'True'
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"""
    ╔════════════════════════════════════════╗
    ║   Image Mutation Tool - Backend API    ║
    ╚════════════════════════════════════════╝
    
    🚀 Server starting...
    📍 Running on http://localhost:{port}
    🔧 Debug mode: {debug}
    
    Available endpoints:
    ✓ GET  /api/health              - Health check
    ✓ GET  /api/mutations           - List mutations
    ✓ POST /api/mutate              - Apply mutation
    ✓ GET  /api/image/<file>        - View result image
    ✓ GET  /api/download/<file>     - Download single result
    ✓ POST /api/download-batch      - Download multiple as ZIP
    
    📚 API Docs: http://localhost:{port}/api/mutations
    
    Press CTRL+C to quit
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
