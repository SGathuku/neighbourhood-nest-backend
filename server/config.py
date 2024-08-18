import cloudinary
import cloudinary.uploader
import cloudinary.api

class Config:
    # Other configurations...
    CLOUDINARY_CLOUD_NAME = 'your_cloud_name'
    CLOUDINARY_API_KEY = 'your_api_key'
    CLOUDINARY_API_SECRET = 'your_api_secret'
    
    @staticmethod
    def init_cloudinary():
        cloudinary.config(
            cloud_name=Config.CLOUDINARY_CLOUD_NAME,
            api_key=Config.CLOUDINARY_API_KEY,
            api_secret=Config.CLOUDINARY_API_SECRET
        )
