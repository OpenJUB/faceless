__author__ = 'twiesing'

from django.core.management.base import BaseCommand
from users.models import UserProfile

import os
import os.path
import shutil

class Command(BaseCommand):
    help = 'Exports the list of people along with their profile pictures. '

    def add_arguments(self, parser):
        parser.add_argument('--folder', help='Folder to export images and '
                                             'data file to. ')

    def handle(self, *args, **options):
        # path to put things in
        folder = os.path.join(os.getcwd(), options['folder'])

        # create the folder
        os.makedirs(folder, exist_ok=True)

        # CSV output
        output = "username,faceless,has_image,filepath"

        # iterate over users
        for user in UserProfile.objects.all():

            # line to put into the CSV
            line = '{},{},{},'.format(user.user.username, user.faceless,
                                     bool(user.image))


            # copy image if it exists
            if user.image:

                _, extension = os.path.splitext(user.image.path)
                filename = '{}{}'.format(user.user.username, extension)
                imagepath = os.path.join(folder, filename)

                shutil.copyfile(user.image.path, imagepath)
                line += filename
                print('Wrote {}'.format(imagepath))

            output += '\n'+line

        # write the csvfile
        csvfile = os.path.join(folder, 'faceless.csv')
        with open(csvfile, 'w') as f:
            f.write(output)
        print('Wrote {}'.format(csvfile))

