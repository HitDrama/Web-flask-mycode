import os
from flask import Flask, render_template, redirect, url_for, flash, request,Blueprint
from shop import db
from shop.models.category import Category
from shop.models.product import Product
from shop.forms.form_product import ProductForm
from werkzeug.utils import secure_filename
import time

pro_route=Blueprint("pro",__name__)

upload_folder = 'shop/static/uploads'
allow_extension = {'png', 'jpg', 'jpeg', 'gif'}

def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allow_extension

#chức năng hiển thị danh sách
@pro_route.route("/")
def index():
    sanpham=Product.query.all() #select * from product
    return render_template("backend/product/list.html",products=sanpham)

# @pro_route.route("/add",methods=['GET','POST'])
# def add():
#     form=ProductForm()
#     form.category_id.choices=[(0,'===select===')] + [ (c.id, c.name) for c in Category.query.all()]
#     if form.validate_on_submit():
#         tenhinh="hinh.jpeg"
#         if 'image' in request.files and allow_file(request.files['image'].filename):
#             hinh=request.files['image'] # kích thước, tên file hinh, đuôi hinh .png...
#             hinhgoc=secure_filename(hinh.filename)
#             chuoi=str(int(time.time())) #thơi gian upload ảnh
#             tenhinh=f'{chuoi}_{hinhgoc}' #172767233_tenhinh.png
#             hinh.save(os.path.join(upload_folder,tenhinh))

#         #thêm sản phẩm
#         sp=Product(
#             name=form.name.data,
#             desc=form.desc.data,
#             price=form.price.data,
#             category_id=form.category_id.data,
#             is_active=form.is_active.data,
#             image=tenhinh
#         )
#         db.session.add(sp)
#         db.session.commit()
#         flash("Thêm sản phẩm thành công","success")
#         return redirect(url_for('sys.pro.index'))
#     return render_template("backend/product/form.html",form=form)

@pro_route.route("/add", methods=['GET', 'POST'])
def add():
    form = ProductForm()
    form.category_id.choices = [(0, '===select===')] + [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        # Kiểm tra category_id
        category_id = form.category_id.data
        if category_id == 0:  # Nếu không chọn danh mục nào, đặt category_id là None
            category_id = None

        tenhinh = "hinh.jpeg"
        if 'image' in request.files and allow_file(request.files['image'].filename):
            hinh = request.files['image']
            hinhgoc = secure_filename(hinh.filename)
            chuoi = str(int(time.time()))
            tenhinh = f'{chuoi}_{hinhgoc}'
            hinh.save(os.path.join(upload_folder, tenhinh))

        # Thêm sản phẩm
        sp = Product(
            name=form.name.data,
            desc=form.desc.data,
            price=form.price.data,
            category_id=category_id,
            is_active=form.is_active.data,
            image=tenhinh
        )

        try:
            db.session.add(sp)
            db.session.commit()
            flash("Thêm sản phẩm thành công", "success")
            return redirect(url_for('sys.pro.index'))
        except Exception as e:
            db.session.rollback()  # Rollback nếu có lỗi
            flash(f"Có lỗi xảy ra: {str(e)}", "danger")

    return render_template("backend/product/form.html", form=form)


@pro_route.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    pro = Product.query.get_or_404(id)
    form = ProductForm(obj = pro)
    form.category_id.choices = [(0, '===select===')] + [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        # Kiểm tra category_id
        category_id = form.category_id.data
        if category_id == 0:  # Nếu không chọn danh mục nào, đặt category_id là None
            category_id = None

        tenhinh = "hinh.jpeg"
        if 'image' in request.files and allow_file(request.files['image'].filename):
            #xoa hinh cu
            hinhcu=pro.image
            duongdan = os.path.join(upload_folder,tenhinh)
            if os.path.isfile(duongdan):
                os.remove(duongdan)
            #cap nhat hinh moi
            hinh = request.files['image']
            hinhgoc = secure_filename(hinh.filename)
            chuoi = str(int(time.time())) # thoi gian upload anh
            tenhinh = f'{chuoi}_{hinhgoc}' # ví du: 1729684576_MSI.png
            hinh.save(os.path.join(upload_folder, tenhinh))
        else:
            tenhinh = pro.image

        # Sửa sản phẩm
      
        pro.name = form.name.data
        pro.desc = form.desc.data
        pro.price = form.price.data
        pro.category_id = category_id
        pro.is_active = form.is_active.data
        pro.image = tenhinh
        

        try:
            db.session.commit()
            flash("Thêm sản phẩm thành công", "success")
            return redirect(url_for('sys.pro.index'))
        except Exception as e:
            db.session.rollback()  # Rollback nếu có lỗi
            flash(f"Có lỗi xảy ra: {str(e)}", "danger")
    return render_template("backend/product/form.html",form=form)

@pro_route.route("/delete/<int:id>")
def delete(id):
    sp = Product.query.get_or_404(id)
    tenhinh=sp.image
    duongdan = os.path.join(upload_folder,tenhinh)
    if os.path.isfile(duongdan):
        os.remove(duongdan)
    db.session.delete(sp)
    db.session.commit()
    flash("Xóa thành công sản phẩm")
    return redirect(url_for('sys.pro.index'))