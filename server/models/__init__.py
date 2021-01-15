from .models import Album, Photos


try:
    Album.create_table()
except:
    pass

try:
    Photos.create_table()
except:
    pass