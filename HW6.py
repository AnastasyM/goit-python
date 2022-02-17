import os
import re
import shutil


def normalize(file_name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
    
    TRANS = {}
    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
      TRANS[ord(c)] = t
      TRANS[ord(c.upper())] = t.upper()

    pre_norm_file_name = file_name.translate(TRANS)      
    pre_norm_file_name_split = re.split('\.', pre_norm_file_name)    
    
    norm_file_name = ''

    for i in pre_norm_file_name_split[0]:      
        p = re.sub('\W', '_', i)
        norm_file_name += p

    return norm_file_name


known_files = {'audios':['.mp3', '.wma', '.ogg'], 'images':['.png', '.jpg', '.jpeg'],
 'documents':['.doc', '.docx', '.txt', '.xlsx', '.pptx'], 
 'video':['.avi', '.mp4', '.mov', '.mkv'], 'archives':['.zip', '.gz', '.tar'], 'unknown':[]}


list_of_known_ext = []
list_of_unknown_ext = []

list_result = {'audios':[], 'images':[], 'documents':[], 'video':[], 'archives':[], 'unknown':[]}


def sort(full_path_to_file, global_path):

    main_path, file = os.path.split(full_path_to_file)
    file_name, file_ext = os.path.splitext(file)
    
    for dir, exts in list_result.items():
        if file_name in dir:
            list_result[dir].append(file_name)

    for dir, exts in known_files.items():
        
        if file_ext in exts:
            list_result[dir].append(file)
            if not os.path.exists(os.path.join(global_path, dir)):
                os.mkdir(os.path.join(global_path, dir))

            path_dir_new = os.path.join(global_path, dir, normalize(file_name))
            path_file_new = os.path.join(global_path, dir, normalize(file_name) + file_ext)               
            os.replace(full_path_to_file, path_file_new)
            
            if dir == 'archives':
                shutil.unpack_archive(path_file_new, path_dir_new)     
                os.remove(path_file_new)
            list_of_known_ext.append(file_ext)
            return print(file_ext, 'known')
            
    if not os.path.exists(os.path.join(global_path, 'unknown')):
        os.mkdir(os.path.join(global_path, 'unknown'))
    os.replace(full_path_to_file, os.path.join(global_path, 'unknown', normalize(file_name) + file_ext))
    list_of_unknown_ext.append(file_ext)
    return print(file_ext, 'unknown')


def walk (path, prev_list_dir, global_path):
    #print (os.getcwd())
    os.chdir(path)
    list_file = os.listdir(path)
    #print (list_file)
    #if len(list_file) == 0:
        #os.remove(path) 

    fullpaths  = map(lambda name: os.path.join(path, name), list_file)
    
    dirs = []
    files = []

    for file in fullpaths:
        if os.path.isdir(file): dirs.append(file)
        if os.path.isfile(file): files.append(file)

    for file in files:
        sort(file, global_path)

    for dir in dirs:
        dirs.remove(dir)
        for entry in os.scandir(dir):
            if os.path.isdir(entry.path) and not os.listdir(entry.path) :
                os.rmdir(entry.path)
        
        walk(fr'{dir}', dirs, global_path)


    return print(list_result, f'known_ext: {set(list_of_known_ext)}', f'unknown_ext: {set(list_of_unknown_ext)}')  



#walk (r'C:\Users\user\Desktop\GoIT_Phyton\DZ\6\TestFolder', [], r'C:\Users\user\Desktop\GoIT_Phyton\DZ\6\TestFolder')


