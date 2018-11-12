import os
import subprocess
import shutil

path_project = '/var/www/python/mturk-manager'

subprocess.run('ls /', shell=True)
subprocess.run('ls /data', shell=True)
subprocess.run('ls /app', shell=True)
path_data = '/data'
path_database = '/data/database1'
name = 'kritten'
password = 'safepassword'
global_init = False

def find_owner(filename):
    return os.stat(filename).st_uid

def main():
    # id_owner = find_owner('/data_corpus')
    # subprocess.run('usermod -u {} www-data'.format(id_owner), shell=True)

    # print(os.getenv('folder_setting_files'))

    # id_corpus = get_id()

    # path_data_corpus = os.path.join(path_data, id_corpus)

    # if not os.path.exists(path_data_corpus):
    #     os.makedirs(path_data_corpus)

    # config_django_urls(id_corpus)
    # config_django_templates()

    change_directory_database()
    subprocess.run("./setup_db.sh", cwd=path_project)
    config_django_settings()

    configure_apache()


    # subprocess.run(["python3", "manage.py", "collectstatic"], cwd=path_project+'/viewer-framework')

    # subprocess.run('chown -R  755 {}'.format(path_project), shell=True)
    subprocess.run('chown -R  www-data:www-data {}'.format(path_project), shell=True)
    # subprocess.run('chown -R  www-data:www-data {}'.format(os.path.join(path_data_corpus, folder_viewer)), shell=True)

    subprocess.run('service apache2 restart', shell=True)


    subprocess.run(["python3"])
    # subprocess.run(["python3", "manage.py", "runserver", "0.0.0.0:8000"], cwd=path_project+'/viewer-framework')

def configure_apache():
    if init == False:
        return 
    print('CONFIGURING APACHE')
    list_lines = []
    with open('/etc/apache2/sites-available/000-default.conf', 'r') as f:
        for index, line in enumerate(f):
            list_lines.append(line)
                            
            if index == 10:
                list_lines.append('ServerName mturk-manager\n')

                # list_lines.append('Alias /static/ {}/viewer-framework/static/\n'.format(path_project))

                # list_lines.append('Alias /favicon.ico {}/viewer-framework/static/favicon.ico\n'.format(path_project))

                # list_lines.append('<Directory path_project/viewer-framework/static>\n')
                # list_lines.append('Require all granted\n')
                # list_lines.append('</Directory>\n')

                # list_lines.append('<Directory {}/>\n'.format(path_project))
                # list_lines.append('Require all granted\n')
                # list_lines.append('</Directory>\n')

                # list_lines.append('<Directory /data/viewer/{}/>\n'.format(id_corpus))
                # list_lines.append('Require all granted\n')
                # list_lines.append('</Directory>\n')

                # list_lines.append('<Directory {}/viewer-framework/viewer-framework/>\n'.format(path_project))
                # list_lines.append('<Files wsgi.py>\n')
                # list_lines.append('Require all granted\n')
                # list_lines.append('</Files>\n')
                # list_lines.append('</Directory>\n')

                list_lines.append('WSGIDaemonProcess mturk-manager python-home=/var/www/python/mturk-manager/mturk_db/ python-path=/var/www/python/mturk-manager/mturk_db/\n')
                # list_lines.append('WSGIDaemonProcess viewer-framework python-home=/home/sammy/myproject/myprojectenv python-path=/home/sammy/myproject\n')
                list_lines.append('WSGIProcessGroup mturk-manager\n')
                list_lines.append('WSGIScriptAlias / /var/www/python/mturk-manager/mturk_db/mturk_db/wsgi.py\n'.format(path_project))
                list_lines.append('WSGIPassAuthorization On\n')

    with open('/etc/apache2/sites-available/000-default.conf', 'w') as f:
        for line in list_lines:
            f.write(line)

# def get_id():
#     dict_settings = load_corpus_from_file(path_file_settings)

#     return dict_settings['id_corpus']

def config_django_settings():
    # path_cache = os.path.join(path_data_corpus, folder_viewer, folder_cache)
    # if not os.path.exists(path_cache):
    #     os.makedirs(path_cache)

    # path_index = os.path.join(path_data_corpus, folder_viewer, folder_index)
    # if not os.path.exists(path_index):
    #     os.makedirs(path_index)
    if init == False:
        return 

    list_lines = []
    is_databases = False
    with open(path_project+'/mturk_db/mturk_db/settings.py', 'r') as f:
        for line in f:
            if is_databases:
                if line.startswith('}'):
                    is_databases = False
            else:
                if line.startswith('DATABASES'):
                    is_databases = True
                    continue

                # if line.startswith('PATH_FILES_CACHE'):
                #     line = 'PATH_FILES_CACHE = "{}"'.format(path_cache)

                # if line.startswith('PATH_FILES_INDEX'):
                #     line = 'PATH_FILES_INDEX = "{}"'.format(path_index)

                if line.startswith('DEBUG'):
                    line = 'DEBUG = False'

                # if line.startswith('ALLOWED_HOSTS'):
                    # line = 'ALLOWED_HOSTS = ["somehost"]'

                # if line.startswith('DASHBOARD_AVAILABLE'):
                #     continue

                list_lines.append(line)


            # if line.startswith('DATABASES'):
            #     is_databases = True
                
            # if not is_databases:
            #     list_lines.append(line)
            # else:
            #     if line.startswith('}'):
            #         is_databases = False

            # if line.startswith('PATH_FILES_CACHE'):
            #     line = 'PATH_FILES_CACHE = "{}"'.format(path_cache)
            #     list_lines.append(line)

            # if line.startswith('PATH_FILES_INDEX'):
            #     line = 'PATH_FILES_INDEX = "{}"'.format(path_index)
            #     list_lines.append(line)


    with open(path_project+'/mturk_db/mturk_db/settings.py', 'w') as f:
        for line in list_lines:
            f.write(line)

        f.write('\nDATABASES = {}\n'.format({
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'HOST': 'localhost',
                'PASSWORD': password,
                'NAME': name,
                'USER': name,
            }
        }))

        # f.write('STATIC_ROOT = os.path.join(BASE_DIR, \'static/\')\n'.format())

    # shutil.copyfile(path_file_settings, os.path.join(path_project+'/settings', '{}.py'.format(id_corpus)))

    # return id_corpus

# def config_django_urls(id_corpus):
#     with open(path_project+'/viewer-framework/viewer-framework/urls.py', 'w') as f:
#         f.write('''
# from django.conf.urls import include, url
# from django.contrib import admin

# urlpatterns = [
#     #url(r'^admin/', admin.site.urls),
#     #url(r'^', include('dashboard.urls')),
#     url(r'^', include('viewer.urls')),
#     #url(r'^example_app/', include('example_app.urls')),
# ]
#         ''')

    # list_lines = []
    # with open(path_project+'/viewer-framework/viewer/urls.py', 'r') as f:
    #     for line in f:
    #         if '<str:id_corpus>' in line:
    #             line = line.replace('<str:id_corpus>\'', '\'')
    #             line = line.replace('<str:id_corpus>/', '')
    #             line = line.replace('name=', '{\'id_corpus\': \''+id_corpus+'\'}, name=')
        
    #             # line = line[:-3]+', {\'id_corpus\': \''+id_corpus+'\'}'+line[-3:]

    #         list_lines.append(line)


    # with open(path_project+'/viewer-framework/viewer/urls.py', 'w') as f:
    #     for line in list_lines:
    #         f.write(line)

# def config_django_templates():

#     content = ''
#     with open(path_project+'/viewer-framework/viewer/templates/viewer/header_navbar.html', 'r') as f:
#         content = f.read()
#         content = content.replace('url \'viewer:index\' id_corpus', 'url \'viewer:index\'')
#         content = content.replace('url \'viewer:view_item\' id_corpus', 'url \'viewer:view_item\'')
#         content = content.replace('url \'viewer:get_page\' id_corpus', 'url \'viewer:get_page\'')
#         content = content.replace('url \'viewer:tags_export\' id_corpus', 'url \'viewer:tags_export\'')
#         content = content.replace('url \'viewer:tags\' id_corpus', 'url \'viewer:tags\'')
#         content = content.replace('url \'viewer:add_token\' id_corpus', 'url \'viewer:add_token\'')
#         content = content.replace('url \'viewer:edit\' id_corpus', 'url \'viewer:edit\'')
        
#     with open(path_project+'/viewer-framework/viewer/templates/viewer/header_navbar.html', 'w') as f:
#         f.write(content)

#     content = ''
#     with open(path_project+'/viewer-framework/viewer/templates/viewer/index.html', 'r') as f:
#         content = f.read()
#         content = content.replace('url \'viewer:index\' id_corpus', 'url \'viewer:index\'')
#         content = content.replace('url \'viewer:view_item\' id_corpus', 'url \'viewer:view_item\'')
#         content = content.replace('url \'viewer:get_page\' id_corpus', 'url \'viewer:get_page\'')
#         content = content.replace('url \'viewer:tags_export\' id_corpus', 'url \'viewer:tags_export\'')
#         content = content.replace('url \'viewer:tags\' id_corpus', 'url \'viewer:tags\'')
#         content = content.replace('url \'viewer:add_token\' id_corpus', 'url \'viewer:add_token\'')
#         content = content.replace('url \'viewer:edit\' id_corpus', 'url \'viewer:edit\'')
        
#     with open(path_project+'/viewer-framework/viewer/templates/viewer/index.html', 'w') as f:
#         f.write(content)

#     content = ''
#     with open(path_project+'/viewer-framework/viewer/templates/viewer/table.html', 'r') as f:
#         content = f.read()
#         content = content.replace('url \'viewer:index\' id_corpus', 'url \'viewer:index\'')
#         content = content.replace('url \'viewer:view_item\' id_corpus', 'url \'viewer:view_item\'')
#         content = content.replace('url \'viewer:get_page\' id_corpus', 'url \'viewer:get_page\'')
#         content = content.replace('url \'viewer:tags_export\' id_corpus', 'url \'viewer:tags_export\'')
#         content = content.replace('url \'viewer:tags\' id_corpus', 'url \'viewer:tags\'')
#         content = content.replace('url \'viewer:add_token\' id_corpus', 'url \'viewer:add_token\'')
#         content = content.replace('url \'viewer:edit\' id_corpus', 'url \'viewer:edit\'')
        
#     with open(path_project+'/viewer-framework/viewer/templates/viewer/table.html', 'w') as f:
#         f.write(content)

#     content = ''
#     with open(path_project+'/viewer-framework/viewer/templates/viewer/tags.html', 'r') as f:
#         content = f.read()
#         content = content.replace('url \'viewer:index\' id_corpus', 'url \'viewer:index\'')
#         content = content.replace('url \'viewer:view_item\' id_corpus', 'url \'viewer:view_item\'')
#         content = content.replace('url \'viewer:get_page\' id_corpus', 'url \'viewer:get_page\'')
#         content = content.replace('url \'viewer:tags_export\' id_corpus', 'url \'viewer:tags_export\'')
#         content = content.replace('url \'viewer:tags\' id_corpus', 'url \'viewer:tags\'')
#         content = content.replace('url \'viewer:add_token\' id_corpus', 'url \'viewer:add_token\'')
#         content = content.replace('url \'viewer:edit\' id_corpus', 'url \'viewer:edit\'')
        
#     with open(path_project+'/viewer-framework/viewer/templates/viewer/tags.html', 'w') as f:
#         f.write(content)

def init_database():
    print('INIT DATABASE')
    subprocess.run("""su -- postgres -c "psql -c \\\"CREATE USER {} WITH PASSWORD '{}';\\\"" """.format(name, password), shell=True)

    subprocess.run("""su -- postgres -c "psql -c \\\"CREATE DATABASE {};\\\"" """.format(name), shell=True)

    subprocess.run("""su -- postgres -c "psql -c \\\"GRANT ALL PRIVILEGES ON DATABASE {} TO {};\\\"" """.format(name, name), shell=True)

def change_directory_database():
    print('CHANGE DIRECTORY DATABASE')
    print(path_database)
    subprocess.run('ls /', shell=True)
    subprocess.run('ls /data', shell=True)
    
    subprocess.run('service postgresql stop', shell=True)
    # shutil.rmtree(path_database)

    if not os.path.exists(path_database):
        print('creating')
        os.mkdir(path_database)
        subprocess.run('chown -R postgres:postgres {}'.format(path_database), shell=True)
        subprocess.run('su -c \'/usr/lib/postgresql/9.5/bin/initdb -D {}\' postgres'.format(path_database), shell=True)
        global_init = True

    list_lines = []
    with open('/etc/postgresql/9.5/main/postgresql.conf', 'r') as f:
        for line in f:
            if line.startswith('data_directory'):
                line = 'data_directory = \'{}\'\n'.format(path_database)

            list_lines.append(line)

    with open('/etc/postgresql/9.5/main/postgresql.conf', 'w') as f:
        for line in list_lines:
            f.write(line)

    subprocess.run('service postgresql start', shell=True)

    if global_init:
        init_database()

# def load_corpus_from_file(file):
#     with open(file, 'r') as f:
#         global_env = {}
#         local_env = {}

#         compiled = compile(f.read(), '<string>', 'exec')
#         exec(compiled, global_env, local_env)

#         print('parsed settings for \'{}\''.format(file))

#     return local_env['DICT_SETTINGS_VIEWER']

main()