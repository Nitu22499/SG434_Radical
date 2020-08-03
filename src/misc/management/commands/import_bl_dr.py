from django.core.management.base import BaseCommand
from profiles.models import User, Block, District

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        east_blocks = ['PAKYONG', 'GANGTOK', 'REGU', 'RHENOCK', 'KHAMDONG', 'RAKDONG TINTEK', 'DUGA', 'RANKA', 'MARTAM', 'PARAKHA']
        west_blocks = ['GYALSHING', 'SORENG', 'KALUK', 'DENTAM', 'DARAMDIN', 'YUKSAM', 'BERMIOK MARTAM', 'CHONGRANG', 'CHUMBONG']
        north_blocks = ['MANGAN', 'CHUNGTHANG','KABI', 'PASSINGDONG']
        south_blocks = ['YANGANG', 'SUMBUK', 'NAMCHI', 'RAVANGLA', 'TEMI', 'JORETHANG', 'SIKKIP', 'NAMTHANG']
        districts = ['east', 'west', 'north', 'south']
        for district in districts:
            user_obj = User()
            user_obj.username = district + '_admin'
            user_obj.set_password('Pass@123')
            user_obj.is_district_admin = True
            user_obj.save()            
            district_obj = District.objects.create(user = user_obj, district_name = district.upper() + ' SIKKIM')

            for block in eval(district + '_blocks'):
                b_user_obj = User()
                b_user_obj.username = block.lower() + '_admin'
                b_user_obj.set_password('Pass@123')
                b_user_obj.is_block_admin = True
                b_user_obj.save()
                block_obj = Block.objects.create(user = b_user_obj, block_name = block, block_district = district_obj)

        User.objects.create_superuser('admin', email='admin@sikkim.com', password='Pass@123')
        print("Done")