import shutil,os, sys, re, argparse




arguments = sys.argv

try:
    kind = arguments[1]
    if kind not in ['edit', 'very_best', 'zip', '4', 'vid', 'print', 'name_all']:
        kind = "1"
        girl_name = arguments[1]
        if "_" not in girl_name and "*" not in girl_name:
            print ("you forgot to use a dash")
            sys.exit()
        girl_name = girl_name.replace("_", " ")
except:
    kind = "best"

if kind == 'commands':
    print("type 1 simply renames all the files in a folder")
    print("best - get best pics")
    print("edit - takes files from trash and puts them back in folder")
    print("type 4 get unnamed pics from trash, needs girl name")
    print("very best")
    print('zip = deletes zip files')
    print('name_all')
    sys.exit()


# kind = 'vid'
# girls = "casting_calls,aden_bianco,alicia_burley,allie_stacy,amber_elise,lauren_love,amy_leigh_andrews,andrea_marie,aryka_lynne,bailey_owens,brittany_rathel,charlie_laine,daniella_mugnolo,cindy_rey,glroia_sol,corin_riggs,crystal_stevens,marlee_may,monica_sims,raquel_pomplun,elisa_bridges,elle_georgia,lauren_love,hanah_owens,hayden_hayes,heidi_rae,isabella_reneaux,jessica_danielle,jillian_beyor,kasey_chambers,kortnie_oconnor,lauren_guillen,lisa_lefebre,malina_rojel,mary_elisha,mary_karola,mckenzie_taylor,michaele_grauke,morgan_grace,nadia_moore,rachel_gibson,reagan_yun,sarah_stokes,talia_kristen,tania_funes,tara_vaughn,taryn_terrell,tierra_lee,tori_black,traci_denee,valerie_cormier,vannessa_jay,demi_fray,carrie_stevens,wendy_hamilton"


temp_directory = '/Users/kylefoley/Downloads/temp/'
vid_directory = temp_directory



def has_all_names(str1, look_for):
    for name in look_for:
        if name not in str1:
            return False
    return True

def get_greatest_num(current_directory):
    numbers = []
    for current_pic in os.listdir(current_directory):
        if current_pic != '.DS_Store':
            if not os.path.isdir(current_directory + current_pic):
                num = re.findall(r"\d+", current_pic)
                if num != []:
                    numbers.append(int(num[0]))

    if numbers == []:
        return 1
    else:
        return max(numbers)


def get_sub_folders(current_folder, old_folders, girl_name):
    current_directory = temp_directory + current_folder
    no_sub_folders = False
    for current_file in os.listdir(current_directory):
        if current_file != '.DS_Store':
            current_file = current_file.lower()
            if current_file == 'standard':
                shutil.rmtree(current_directory + "/" + "standard")
            elif os.path.isdir(current_directory + "/" + current_file):
                old_folders.append(current_directory + "/" + current_file)
                no_sub_folders = True
    if not no_sub_folders:
        old_folders.append(current_directory)

    return


def find_files_which_starts_with(look_for, this_directory, girl_name):
    new_folder = ""
    delete_these_folders = []
    old_folders = []
    done = False
    greatest_num = 1
    for current_file in os.listdir(this_directory):
        if current_file != '.DS_Store':
            current_file = current_file.lower()
            filename, file_extension = os.path.splitext(current_file)
            # if file_extension == '.zip':
            #     os.unlink(temp_directory + current_file)

            if has_all_names(current_file, look_for) and os.path.isdir(this_directory + current_file):

                if current_file == girl_name and not done:
                    greatest_num = get_greatest_num(temp_directory + current_file)
                    done = True
                    new_folder = temp_directory + girl_name


                else:
                    get_sub_folders(current_file, old_folders, girl_name)
                    delete_these_folders.append(temp_directory + current_file)




    if not done:
        greatest_num = 1
        os.mkdir(temp_directory + girl_name)
        new_folder = temp_directory + girl_name
    if old_folders == []:
        raise Exception ('girl not found')

    return new_folder, delete_these_folders, greatest_num, old_folders

def rename_and_move(old_folders, new_folder, girl_name, greatest_num):
    ext_found = False
    num = greatest_num
    j = 0
    for old_folder in old_folders:
        j += 1
        print (str(j))


        for current_file in os.listdir(old_folder):
            if current_file != '.DS_Store':
                current_file = current_file.lower()
                if not ext_found:
                    full_path_of_current_file = new_folder + current_file
                    list2 = full_path_of_current_file.split(".")
                    exten = list2[-1]
                    ext_found = True
                num += 1
                full_path_of_new_file = new_folder + "/" + girl_name + str(num) + "." + exten
                full_path_of_current_file = old_folder + "/" + current_file
                shutil.copy2(full_path_of_current_file, full_path_of_new_file)


def empty_trash():
    os.chdir('/Users/kylefoley/.Trash')
    if len(sys.argv) >= 2:
        if sys.argv[1] == '-t' or sys.argv[1] == '-T':
            os.system("tree ./")
        elif sys.argv[1] == '-l' or sys.argv[1] == '-L':
            os.system("ls -al")
    os.system("rm -rf *")




if kind == 'name_all':
    for current_file in os.listdir(temp_directory):
        if current_file != '.DS_Store':
            current_file = current_file.lower()
            if os.path.isdir(temp_directory + current_file):
                print (current_file)



elif kind == "1":
    # girl_name = input("girl name: ")
    list1 = girl_name.split(",")
    for girl_name in list1:
        print (girl_name)
        look_for = girl_name.split(" ")
        _ = find_files_which_starts_with(look_for, temp_directory, girl_name)
        new_folder, delete_these_folders, greatest_num, old_folders = _
        rename_and_move(old_folders, new_folder, girl_name, greatest_num)
        for old_folder in delete_these_folders: shutil.rmtree(old_folder)






elif kind in ['best', "edit", "very_best"]:

    trash = "/Users/kylefoley/.Trash/"



    new_folder = []
    for current_file in os.listdir(trash):
        if current_file != '.DS_Store':
            new_folder.append(current_file)

    name, ext = os.path.splitext(new_folder[0])
    name = re.sub("\d+", " ", name)
    name = name.strip()
    if not os.path.exists(temp_directory + name):
        raise Exception ("she does not have a folder yet")

    else:
        if not os.path.exists(temp_directory + name + "/" + "best") and kind == "best":
            os.mkdir(temp_directory  + name + "/" + "best")


        if kind == "best":
            best = temp_directory + name + "/" + "best"
            for current_file in new_folder:
                shutil.copy2(trash + current_file, best + "/" + current_file)
                shutil.copy2(trash + current_file, temp_directory + name + "/" + current_file)
        elif kind == 'very_best':

            very_best = temp_directory + name + "/" + "very_best"
            if not os.path.exists(very_best):
                os.mkdir(very_best)

            best = temp_directory + name + "/" + "best"
            for current_file in new_folder:
                shutil.copy2(trash + current_file, best + "/" + current_file)
                shutil.copy2(trash + current_file, very_best + "/" + current_file)


        else:
            highest = get_greatest_num(trash)
            target_directory = temp_directory + name
            to_be_deleted = []
            for current_file in os.listdir(target_directory):
                if current_file != '.DS_Store' and \
                not os.path.isdir(target_directory + "/" + current_file):


                    num = re.findall("\d+", current_file)
                    if int(num[0]) < highest:
                        to_be_deleted.append(target_directory + "/" + current_file)

            for current_file in new_folder:
                shutil.copy2(trash + "/" + current_file, temp_directory + "/" + name + "/" + current_file)
            for current_file in to_be_deleted:
                os.unlink(current_file)


elif kind == "4":
    # girl_name = 'louise glover'

    assert os.path.exists(temp_directory + "/" + girl_name)

    greatest_num = get_greatest_num(temp_directory + girl_name)
    trash = "/Users/kylefoley/.Trash/"

    rename_and_move([trash], temp_directory + girl_name, girl_name, greatest_num)



elif kind == 'zip':
    for current_file in os.listdir(temp_directory):
        if current_file != '.DS_Store':
            current_file = current_file.lower()
            filename, file_extension = os.path.splitext(current_file)
            if file_extension == '.zip':
                os.unlink(temp_directory + current_file)


elif kind == 'vid':
    try:
        girls = arguments[2]
        girls = girls.replace("_", " ")
        girls = girls.split(",")

    except:
        girls = []
    for current_file in os.listdir(temp_directory):
        if current_file != '.DS_Store':
            current_file = current_file.lower()
            if os.path.isdir(temp_directory + current_file):
                girls.append(current_file)

    for current_file in os.listdir(vid_directory):
        filename, file_extension = os.path.splitext(current_file)
        if file_extension in ['.mp4', '.avi', '.wmv', '.mov', '.m4v', ".crdownload"]:
            list1 = re.split("[-_ ]+", filename)
            list1 = [x.lower() for x in list1]

            for girl in girls:
                if not os.path.exists(temp_directory + girl):
                    os.mkdir(temp_directory + girl)

                list2 = girl.split(" ")
                if all(i in list1 for i in list2):
                    print (girl)
                    if not os.path.exists(temp_directory + girl + "/" + "vid/"):
                        os.mkdir(temp_directory + girl + "/" + "vid/")

                    shutil.copy2(vid_directory + current_file, temp_directory + girl + "/" + "vid/" + current_file)
                    os.unlink(vid_directory + current_file)
                    break
    bb = 8









empty_trash()
print ("done")


