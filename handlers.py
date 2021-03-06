import time
import os
import shutil
import zipfile

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from dao import ud
from dao import ui
from dao import ad
from dao import adm
from dao import hd
from dao import sbd
from dao import rd
from dao import md

# TODO: split this file


class logoutHandler(tornado.web.RequestHandler):
    """docstring for logoutHandler"""

    def get(self):
        self.clear_cookie('stuID')
        self.redirect('/')


class aboutHandler(tornado.web.RequestHandler):
    """docstring for aboutHandler"""

    def get(self):
        username = self.get_cookie('stuID')
        self.render('error.html', cookie_name=username,
                    messages=md.fetch_message(username))


class eggsHandler(tornado.web.RequestHandler):
    """docstring for eggHandler"""

    def get(self):
        username = self.get_cookie('stuID')
        self.render('eggs.html', cookie_name=username,
                    messages=md.fetch_message(username))


class messageHandler(tornado.web.RequestHandler):
    """docstring for messageHandler"""

    def post(self):
        username = self.get_cookie('stuID')
        if not username:
            self.redirect('/error')

        recevier_name = self.get_argument('receiver_name')
        content = self.get_argument('message_content')
        md.insert(username, recevier_name, '', content,
                  time.strftime('%Y-%m-%d %H:%M:%S'))
        self.redirect('/')


class indexHandler(tornado.web.RequestHandler):

    def get(self):
        username = self.get_cookie('stuID')
        self.render('index.html',
                    cookie_name=username,
                    is_admin=adm.is_admin(username),
                    announcements=ad.fetch_all(),
                    messages=md.fetch_message(username))

    def post(self):
        '''login'''
        name = self.get_argument('username')
        password = self.get_argument('password')
        res = ud.check_pass(name, password)
        if res:
            self.set_cookie('stuID', name)
            # TODO: set cookie time
            # TODO: set secure cookie
            self.redirect('/')
        else:
            pass
            # TODO(lxiange): wrong password
            self.redirect('/')


class registerHandler(tornado.web.RequestHandler):
    """Doc:
    handle regist information
    """

    def get(self):
        username = self.get_cookie('stuID')
        self.render('register.html', same_name=False, cookie_name=username,
                    messages=[])

    def post(self):
        name = self.get_argument('username')
        password = self.get_argument('password')
        njuid = self.get_argument('njuid')

        res = ud.user_exist(name)
        if res:  # user exists
            username = self.get_cookie('stuID')
            self.render('register.html', same_name=True, cookie_name=username,
                        messages=[])
        else:
            ud.insert(name, password, njuid, 'stu')
            ui.insert(name, '', '', '', '', '')
            self.set_cookie('stuID', name)
            self.redirect('/setting')


class settingHandler(tornado.web.RequestHandler):
    '''edit user infomation'''

    # TODO(lxiange): user photos

    def get(self):
        username = self.get_cookie('stuID')
        if not username:
            self.redirect('/error')

        userinfo = ui.fetch(username)
        info_args = ['username', 'sex', 'email', 'truename', 'mobile', 'self_intro']
        info_dict = {}
        for item in info_args:
            try:
                info_dict[item] = userinfo[item]
            except Exception as e:
                print(e)
                info_dict[item] = ''

        njuid = ud.fetch(username)['njuid']
        self.render(
            'setting.html',
            cookie_name=username,
            is_admin=adm.is_admin(username),
            njuid=njuid,
            messages=md.fetch_message(username),
            **info_dict
        )

    def post(self):
        '''modify'''
        # assert self.get_cookie('stuID') == self.get_argument('username')
        username = self.get_cookie('stuID')
        if not username:
            self.redirect('/error')

        info_args = ['sex', 'email', 'truename', 'mobile', 'self_intro']
        info_dict = {}
        for item in info_args:
            try:
                info_dict[item] = self.get_argument(item)
            except Exception as e:
                print(e)
                info_dict[item] = ''

        ui.update(username, info_dict)
        self.redirect('/')


class manageHandler(tornado.web.RequestHandler):
    '''handler for admin to manage'''

    # not well, should use post instead.
    def get(self, para):
        username = self.get_cookie('stuID')
        if not adm.is_admin(username):
            self.redirect('/error')

        if para == 'add_admin':
            adm.set_TA(self.get_argument('username'))
            self.redirect('/member')

        if para == 'delete_user':
            adm.delete_user(self.get_argument('username'))
            self.redirect('/member')


class submitHomeworkHandler(tornado.web.RequestHandler):
    '''handler for submit homework'''

    def get(self):
        username = self.get_cookie('stuID')
        if not username:
            self.redirect('/error')

        homework_id = int(self.get_argument('hw_id', '0'))
        if homework_id == 0:
            # cann't get homework id
            self.redirect('/error')

        homework_info = hd.fetch_by_id(homework_id)
        assert homework_info
        status = 'notsubmit'
        submission = sbd.fetch_one_submission(username, homework_id)
        if not submission:
            status = 'notsubmit'
        else:
            status = submission['status']
        self.render('submit_homework.html', cookie_name=username,
                    is_admin=adm.is_admin(username),
                    homework_info=homework_info,
                    status=status,
                    messages=md.fetch_message(username))

    def post(self):
        username = self.get_cookie('stuID')
        if not username:
            self.redirect('/error')
        submission_content = self.get_argument('submission_content')
        submission_files = self.request.files.get('submission_files')
        homework_id = int(self.get_argument('hw_id', '0'))

        filepath = ''
        if submission_files:
            assert len(submission_files) == 1
            for sb_file in submission_files:
                filename = sb_file['filename']
                # TODO: try catch
                filepath = os.path.join(
                    'data', 'homework', 'hw_' + str(homework_id), filename)
                # TODO: this method is unsafe, handle the comflict.
                with open(filepath, 'wb') as upfile:
                    upfile.write(sb_file['body'])
        # TODO: find a better file upload way.
        sbd.insert(username, '', submission_content,
                   time.strftime('%Y-%m-%d %H:%M:%S'),
                   homework_id, filepath, 'submitted')
        # title is ''

        self.render('eggs.html', cookie_name=username,
                    messages=md.fetch_message(username))


class announcementHandler(tornado.web.RequestHandler):
    '''post an announcement, only admin can do this'''

    def get(self):
        username = self.get_cookie('stuID')
        if not adm.is_admin(username):
            self.redirect('/error')

        self.render('announcement.html', cookie_name=username,
                    is_admin=adm.is_admin(username),
                    messages=md.fetch_message(username))

    def post(self):
        '''only admin can post'''
        username = self.get_cookie('stuID')
        if not adm.is_admin(username):
            self.redirect('/error')
        title = self.get_argument('announcement_title')
        author = username
        content = self.get_argument('announcement_content')
        date_ = time.strftime('%Y-%m-%d %H:%M:%S')

        ad.insert(title, author, content, date_)
        self.redirect('/')


class homeworkHandler(tornado.web.RequestHandler):
    """assign a homework or view homework"""

    def get(self, para):
        username = self.get_cookie('stuID')
        if not username:
            self.redirect('/error')

        if para == 'view':
            homework_list = hd.fetch_all()
            status_dict = {}
            enable_submit = {}   # True or False
            for hw in homework_list:
                hw_id = hw['homework_id']
                assert hw_id
                submission = sbd.fetch_one_submission(username, hw_id)
                if not submission:
                    status_dict[hw_id] = 'notsubmit'
                else:
                    status_dict[hw_id] = submission['status']
                    assert status_dict[hw_id] != 'notsubmit'

                ddl = time.mktime(time.strptime(hw['deadline'], '%Y-%m-%d %H:%M:%S'))
                now = time.mktime(time.localtime())
                is_enable = now - ddl < 0
                enable_submit[hw_id] = is_enable

            self.render('homework.html', cookie_name=username,
                        homework_list=homework_list,
                        is_admin=adm.is_admin(username),
                        status_dict=status_dict,
                        enable_submit=enable_submit,
                        messages=md.fetch_message(username))

        if para == 'assign':
            if not adm.is_admin(username):
                self.redirect('/error')
            self.render('assign_homework.html', cookie_name=username,
                        is_admin=adm.is_admin(username),
                        messages=md.fetch_message(username))

        if para == 'delete':
            if not adm.is_admin(username):
                self.redirect('/error')
            homework_id = int(self.get_argument('hw_id'))
            hd.delete(homework_id)
            shutil.rmtree(os.path.join('data', 'homework', 'hw_' + str(homework_id)))
            self.redirect('/homework/view')

    def post(self, para):
        if para == 'view':
            self.redirect('/error')
        # only assign_homework accept post request
        username = self.get_cookie('stuID')
        if not adm.is_admin(username):
            self.redirect('/error')

        title = self.get_argument('homework_title')
        author = username
        content = self.get_argument('homework_content')
        date_ = time.strftime('%Y-%m-%d %H:%M:%S')
        deadline = self.get_argument('homework_deadline', '2013-01-08 23:57:32')
        hd.insert(title, author, content, date_, deadline)
        homework_id = hd.get_last_id()
        # TODO: try catch
        os.mkdir(os.path.join('data', 'homework', 'hw_' + str(homework_id)))
        self.redirect('/homework/view')


class resourceHandler(tornado.web.RequestHandler):
    """docstring for resourceHandler"""

    def get(self):
        username = self.get_cookie('stuID')
        if not username:
            self.redirect('/error')

        resource_list = rd.fetch_all()

        self.render('resource.html', cookie_name=username,
                    is_admin=adm.is_admin(username),
                    resource_list=resource_list,
                    messages=md.fetch_message(username))


class downloadHandler(tornado.web.RequestHandler):
    """docstring for downloadHandler"""

    def get(self, para):
        username = self.get_cookie('stuID')
        if not username:
            self.redirect('/error')

        assert para in ['resource', 'homework', 'submission']
        if para == 'resource':
            data_id = int(self.get_argument('res_id'))
            data = rd.fetch_by_id(data_id)

            self.set_header('Content-Type', 'application/octet-stream')
            filename = os.path.basename(data['file_path'])
            self.set_header('Content-Disposition',
                            'attachment; filename=' + filename)
            with open(data['file_path'], 'rb') as f:
                self.write(f.read())

        if para == 'homework':
            # TODO: find a better way to download zip file
            if not adm.is_admin(username):
                self.redirect('/error')
            homework_id = int(self.get_argument('hw_id'))
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition',
                            'attachment; filename=hw_' + str(homework_id) + '.zip')
            zfile = zipfile.ZipFile('temp.zip', 'w')
            startdir = './data/homework/hw_' + str(homework_id)
            for dirpath, dirnames, filenames in os.walk(startdir):
                for filename in filenames:
                    zfile.write(os.path.join(dirpath, filename))
            zfile.close()
            with open('temp.zip', 'rb') as f:
                self.write(f.read())


class uploadResourceHandler(tornado.web.RequestHandler):
    """docstring for uploadResourceHandler"""

    def get(self):
        username = self.get_cookie('stuID')
        if not adm.is_admin(username):
            self.redirect('/error')

        self.render('upload_resource.html', cookie_name=username,
                    is_admin=adm.is_admin(username),
                    messages=md.fetch_message(username))

    def post(self):
        username = self.get_cookie('stuID')
        if not adm.is_admin(username):
            self.redirect('/error')

        title = self.get_argument('resource_title')
        author = username
        content = self.get_argument('resource_content')
        date_ = time.strftime('%Y-%m-%d %H:%M:%S')

        resource_id = rd.get_last_id()
        filepath = ''
        resource_files = self.request.files.get('resource_files')
        if resource_files:
            os.mkdir(os.path.join('data', 'resource', 'res_' + str(resource_id)))
            assert len(resource_files) == 1
            for res_file in resource_files:
                filename = res_file['filename']
                # TODO: try catch
                filepath = os.path.join(
                    'data', 'resource', 'res_' + str(resource_id), filename)
                # TODO: this method is unsafe, handle the comflict.
                with open(filepath, 'wb') as upfile:
                    upfile.write(res_file['body'])
        # TODO: find a better file upload way.

        rd.insert(author, title, content, date_, filepath)
        # TODO: homework is (title, author, ...), unify them.
        self.redirect('/resource')


class errorHandler(tornado.web.RequestHandler):

    def get(self):
        username = self.get_cookie('stuID')
        self.render('error.html', cookie_name=username,
                    messages=md.fetch_message(username))

    def post(self):
        self.redirect('/error')


class memberHandler(tornado.web.RequestHandler):

    def get(self):
        username = self.get_cookie('stuID')
        if not username:
            self.redirect('/error')

        user_info_list = ui.fetch_member_info()
        self.render('member.html', cookie_name=username,
                    is_admin=adm.is_admin(username),
                    user_info_list=user_info_list,
                    messages=md.fetch_message(username))

    def post(self):
        username = self.get_cookie('stuID')
        if not adm.is_admin(username):
            self.redirect('/error')

        # TODO: del or send message or set TA
