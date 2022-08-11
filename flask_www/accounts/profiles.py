import os
import shutil

from flask import Blueprint, g, redirect, url_for, render_template, request, abort
from flask_login import current_user

from flask_www.accounts.forms import ProfileForm, VendorForm
from flask_www.accounts.models import Profile, User, LEVELS
from flask_www.accounts.utils import login_required, send_mail_for_any
from flask_www.commons.ownership_required import profile_ownership_required
from flask_www.commons.utils import save_file
from flask_www.configs import db
from flask_www.configs.config import NOW, BASE_DIR

NAME = 'profiles'
profiles_bp = Blueprint(NAME, __name__, url_prefix='/accounts')


@profiles_bp.route('/profile/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProfileForm()
    nickname = form.nickname.data
    message = form.message.data
    profile_image = form.data.get('profile_image')
    print(profile_image)
    # profile_image = request.files.get('profile_image')
    if form.validate_on_submit():
        new_profile = Profile(
            nickname=nickname,
            message=message,
            user_id=g.user.id
        )
        if profile_image:
            relative_path, _ = save_file(NOW, profile_image)
            new_profile.image_path = relative_path
            print(new_profile.image_path)
        db.session.add(new_profile)
        db.session.commit()
        return redirect(url_for('profiles.detail', _id=new_profile.id))
    # else:
    #     flash('이미 등록한 닉네임이 있습니다.')
    return render_template('accounts/profiles/profile_create.html', form=form)


@profiles_bp.route('/profile/detail/<int:_id>', methods=['GET'])
def detail(_id):
    profile_obj = db.session.query(Profile).filter_by(id=_id).first()
    user_id = profile_obj.user_id
    user_obj = User.query.get_or_404(user_id)
    return render_template('accounts/profiles/profile_detail.html', profile_user=user_obj, profile=profile_obj)


@profiles_bp.route('/profile/vendor/not', methods=['GET', 'POST'])
@login_required
def vendor_not():
    _id = current_user.id
    user_obj = User.query.get_or_404(_id)
    profile_obj = Profile.query.filter_by(user_id=user_obj.id).first()
    return render_template('accounts/profiles/vendor_not.html', user=user_obj, profile=profile_obj)


@profiles_bp.route('/profile/update/<int:_id>', methods=['GET', 'POST'])
@profile_ownership_required
def update(_id):
    form = ProfileForm(request.form)
    profile = db.session.query(Profile).filter_by(id=_id).one()
    if request.method == 'POST':
        if profile:
            profile.nickname = form.nickname.data
            profile.message = form.message.data
            # profile_image = form.data.get('profile_image')
            profile_image = request.files.get('profile_image')
            if profile_image:
                profile_image_relative_path, profile_image_upload_path = save_file(NOW, profile_image)
                if profile.image_path:
                    profile_image_origin_path = os.path.join(BASE_DIR, profile.image_path)
                    if profile_image_origin_path != profile_image_upload_path:
                        if os.path.isfile(profile_image_origin_path):
                            shutil.rmtree(os.path.dirname(profile_image_origin_path))
                profile.image_path = profile_image_relative_path
                db.session.add(profile)
                db.session.commit()
            return redirect(url_for('profiles.detail', _id=_id))
    return render_template('accounts/profiles/profile_update.html', form=form, getprofile=profile)


@profiles_bp.route('profile/vendor/detail/<int:_id>', methods=['GET'])
@login_required
def vendor_detail(_id):
    # board = TestBoard.query.get_or_404(_id)
    profile_obj = db.session.query(Profile).filter_by(id=_id).first()
    user_id = profile_obj.user_id
    user_obj = User.query.get_or_404(user_id)
    return render_template('accounts/profiles/vendor_detail.html', profile_user=user_obj, profile=profile_obj)


@profiles_bp.route('profile/vendor/update/<int:_id>', methods=['GET', 'POST'])
@profile_ownership_required
def vendor_update(_id):
    form = VendorForm(request.form)
    profile = db.session.query(Profile).filter_by(id=_id).one()
    level = profile.nickname + '[' + profile.level + ']' + ':vendor-register'
    if request.method == 'POST':
        if profile:
            profile.nickname = form.nickname.data
            profile.message = form.message.data
            req_level = request.form.get('level')
            if req_level == level:
                profile.level = LEVELS[1]
            # profile_image = form.data.get('profile_image')
            profile_image = request.files.get('profile_image')
            if profile_image:
                profile_image_relative_path, profile_image_upload_path = save_file(NOW, profile_image)
                if profile.image_path:
                    profile_image_origin_path = os.path.join(BASE_DIR, profile.image_path)
                    if profile_image_origin_path != profile_image_upload_path:
                        if os.path.isfile(profile_image_origin_path):
                            shutil.rmtree(os.path.dirname(profile_image_origin_path))
                profile.image_path = profile_image_relative_path

            profile.corp_email = form.corp_email.data
            profile.corp_number = form.corp_number.data

            corp_image = request.files.get('corp_image')
            if corp_image:
                corp_image_relative_path, corp_image_upload_path = save_file(NOW, corp_image)
                if profile.corp_image_path:
                    corp_image_origin_path = os.path.join(BASE_DIR, profile.corp_image_path)
                    if corp_image_origin_path != corp_image_upload_path:
                        if os.path.isfile(corp_image_origin_path):
                            shutil.rmtree(os.path.dirname(corp_image_origin_path))
                profile.corp_image_path = corp_image_relative_path

            profile.corp_address = form.corp_address.data
            profile.main_phonenumber = form.main_phonenumber.data
            profile.main_cellphone = form.main_cellphone.data
            db.session.add(profile)
            db.session.commit()

            subject = "판매사업자 신청 메일"
            user_email = current_user.email
            token = None
            msg_txt = 'accounts/send_mails/account_update_register_mail.txt'
            msg_html = 'accounts/send_mails/account_update_register_mail.html'
            send_mail_for_any(subject, user_email, token, msg_txt, msg_html)
            return redirect(url_for('profiles.vendor_detail', _id=_id))
    return render_template('accounts/profiles/vendor_update.html', form=form, getprofile=profile, level=level)


@profiles_bp.route('/profile/delete/<int:_id>', methods=['GET', 'POST'])
@profile_ownership_required
def delete(_id):
    profile = db.session.query(Profile).filter_by(id=_id).one()
    if request.method == 'POST':
        if profile:
            try:
                os.unlink(profile.image_path)
            except Exception as e:
                print(e)
            db.session.delete(profile)
            db.session.commit()
            return redirect(url_for('accounts.resetting'))
        abort(404)

    return render_template('accounts/profiles/profile_delete.html', profile=profile)