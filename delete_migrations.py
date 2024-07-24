import os
import glob

# 프로젝트 루트 디렉토리로 변경
os.chdir('C:/Users/fores/Documents/Github/2024OpenSW-BACK') #여기에 본인의 디렉토리를 넣어주면 됩니다. 저는 터미널에서 복붙했어요

# 앱 디렉토리 리스트
apps = ['books', 'dialogs', 'users', 'mypages', 'quizzes']  # 여기에 앱 이름 추가

for app in apps:
    migration_files = glob.glob(f'./{app}/migrations/[!__init__]*.py')
    for file in migration_files:
        os.remove(file)
        print(f'Deleted: {file}')
    pyc_files = glob.glob(f'./{app}/migrations/*.pyc')
    for file in pyc_files:
        os.remove(file)
        print(f'Deleted: {file}')
