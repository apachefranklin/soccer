import os
class FileService:
    def __init__(self, *args, **kwargs):
        pass
    @classmethod
    def validate_file_size(cls,file,max_size=1024*1024*16):
        size=file.size
        if size>max_size:
            return False
        return True

    @classmethod
    def move_upload(cls,file_request,save_path,max_size=1024*1024*3):
        if cls.validate_file_size(file_request,max_size):
            with open(save_path, 'wb+') as destination:
                for chunk in file_request.chunks():
                    destination.write(chunk)
            return True
        return False

    
    @classmethod
    def remove_file(cls,filepath):
        """delete file pass like argument"""
        status=True
        try:
            os.remove(filepath)
        except Exception as e:
            ##print(e)
            status=False
        
        return status
    @classmethod
    def get_extension(cls,file_name):
        split_t=file_name.split(".")
        return split_t[-1]