import os
import uuid

def get_random_filename(instance, filename):
    ext = filename.split('.')[-1]
    random_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('media/', random_filename)