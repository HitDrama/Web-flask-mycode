from flask import render_template, Blueprint,request,redirect,url_for,Response,session,jsonify,flash
from shop.models.menu import MenuItem
from shop.models.product import Product
from shop.models.category import Category
from datetime import datetime
from shop.utils import generate_slug
from shop.forms.form_profile import ProfileForm
from shop.models.account import Account
from flask_login import current_user,login_required
from shop import bcrypt,db
import os
from werkzeug.utils import secure_filename
import time
from shop.models.product import Order,OrderDetail


h_route=Blueprint("home",__name__,template_folder='../../templates/frontend')


def menu_list(items):
    html=''
    for item in items:
        if item.is_active:
            if item.children.count()>0:
                #hiển thị dropdown
                html+=f'''
                    <div class="nav-item dropdown">
                        <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown">{item.name}</a>
                        <div class="dropdown-menu m-0 bg-secondary rounded-0">
                            {menu_list(item.children)}                            
                        </div>
                    </div>
                '''
            else:
                html+=f'<a href="{item.url}" class="nav-item nav-link">{item.name}</a>'
    return html


@h_route.route("/")
def index():
    try:
        title = "Trang chủ"
        keyword = "Trang chủ"
        desc = "Trang chủ"
        menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).order_by(MenuItem.order).all()  #menu cha
        menu_home = menu_list(menu_item)
        list_all= (
        Product.query.filter(Product.is_active==True).order_by(Product.create_at.desc()).limit(8).all()
        )
        list_1 = (
        Product.query.filter(Product.category_id == 26).order_by(Product.create_at.desc()).limit(8).all()
        )
        list_2 = (
        Product.query.filter(Product.category_id == 27).order_by(Product.create_at.desc()).limit(8).all()
        )
        list_3 = (
        Product.query.filter(Product.category_id == 38).order_by(Product.create_at.desc()).limit(8).all()
        )
        list_4 = (
        Product.query.filter(Product.category_id == 39).order_by(Product.create_at.desc()).limit(8).all()
        )
        return render_template("pages/home.html",**locals())
    except Exception as e:
        print(e)
        return redirect(url_for("home.notfound"))

@h_route.route("/category")
def category():
    try:
        title = "Danh mục "
        keyword = "Danh mục "
        desc = "Danh mục "
        menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).order_by(MenuItem.order).all()
        menu_home=menu_list(menu_item)
        #lấy tất cả sản phẩm có is_active=True
        query=Product.query.filter_by(is_active=True)
        #phân trang
        page=request.args.get('page',1,type=int)
        per_page=6
        
        
        #tim kiem theo tu khoa
        tim=request.args.get('search')
        if tim:
            query = query.filter(Product.name.ilike(f"%{tim}%"))

        #tim kiem theo category
        cate = Category.query.all()
        id_danhmuc=request.args.get('cat_id',type=int)
        if id_danhmuc:
            query = query.filter_by(category_id=id_danhmuc)

        #lấy sản phẩm featured
        feature = Product.query.filter_by(is_active=True).order_by(Product.create_at.desc()).limit(3).all()

        #tìm kiếm theo sort
        sapxep=request.args.get('sort')
        if sapxep == 'price_asc':
            query = query.order_by(Product.price.asc())
        elif sapxep == 'price_desc':
            query = query.order_by(Product.price.desc())
        elif sapxep == 'date_asc':
            query = query.order_by(Product.create_at.desc())
        elif sapxep == 'date_desc':
            query = query.order_by(Product.create_at.asc())


        #tìm kiếm theo giá
        min_p=request.args.get('min_price',type=int)
        max_p=request.args.get('max_price',type=int)
        #nếu có giá trị min_price và max_price thì lọc sản phẩm theo giá
        if min_p :
            query = query.filter(Product.price >= min_p)
        if max_p :
            query = query.filter(Product.price <= max_p)

            
        product_list=query.paginate(page=page,per_page=per_page)
        sanpham=product_list.items
        pages = product_list.pages    
            
        return render_template("pages/category.html",**locals())

    except Exception as e:
        print(e)
        return redirect(url_for("home.notfound"))
    
@h_route.route("/not-found")
def notfound():
    menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).all()  #menu cha
    return render_template("pages/notfound.html",menu_home=menu_list(menu_item))

@h_route.route("/<name>-<int:id>")  #https://vnexpress.net/hien-truong-may-bay-yak-130-roi-o-dak-lak-4813837
def product(name,id):
    try:
        menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).all()  #menu cha
        menu_home=menu_list(menu_item)

        #load sản phẩm theo id
        sp= Product.query.get_or_404(id)
        # load danh mục sản phẩm
        cate= Category.query.all()
        

        #seo
        title = sp.name
        keyword = sp.name
        desc = sp.desc

        #hot product
        hot = Product.query.filter(Product.is_active==True).limit(5).all()
        splienquan = Product.query.filter(Product.category_id == sp.category_id,
                                            Product.id != sp.id,
                                            Product.is_active ==True
                                            ).limit(8).all()

        return render_template("pages/product.html",**locals())
    except Exception as e:
        print(e)
        return redirect(url_for("home.notfound"))
    

@h_route.route("/sitemap.xml")  
def sitemap():
    sanpham=Product.query.filter_by(is_active=True).all()    #lấy tất sản phẩm
    danhmuc=Category.query.filter_by(is_active=True).all()   #lấy tất danh mục

    baseurl="http://127.0.0.1:5000"  #tên miền (domain)

    xml=[]
    xml.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml.append('<?xml-stylesheet type="text/xsl" href="shop/static/sitemap.xsl"?>')
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    #tạo url xml trang chủ
    xml.append(f""" 
        <url>
               <loc>{baseurl}</loc>
               <lastmod>{datetime.utcnow().date()}</lastmod>
               <changefreq>daily</changefreq>
               <priority>1.0</priority>
        </url>       
    """)

    #tạo url xml danh mục
    for cate in danhmuc:
        cate_url=url_for("home.category",cat_id=cate.id)
        xml.append(f""" 
            <url>
                <loc>{baseurl}{cate_url}</loc>
                <lastmod>{cate.update_at.date()}</lastmod>
                <changefreq>daily</changefreq>
                <priority>0.9</priority>
            </url>       
        """)
    
    #tạo url xml danh mục
    for sp in sanpham:
        sp_url=url_for("home.product",name=generate_slug(sp.name), id=sp.id)
        xml.append(f""" 
            <url>
                <loc>{baseurl}{sp_url}</loc>
                <lastmod>{sp.update_at.date()}</lastmod>
                <changefreq>daily</changefreq>
                <priority>0.8</priority>
            </url>       
        """)

    xml.append('</urlset>')

    res=Response("\n".join(xml),mimetype='application/xml')
    res.headers['Content-Type']='application/xml; charset=utf-8'
    return res

@h_route.route("/add-to-cart",methods=['POST'])
def cart():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity',1)

    if 'cart' not in session:
        session['cart']={} #tạo giỏ hàng rỗng

    giohang=session['cart'] #lấy giỏ hàng từ 
    
    if str(product_id) in giohang:
        giohang[str(product_id)]['quantity']+=quantity
    else:
        product=Product.query.get(product_id)
        if product:
            giohang[str(product_id)]={'name':product.name,'price':product.price,'quantity':quantity,'image':product.image}
        else:
            return jsonify({'status':'error','message':'Sản phẩm không tồn tại'}),400
        
    session['cart']=giohang
    session.modified = True
    return jsonify({'status':'success','message':'Thêm vào giỏ hàng thành công','cart': giohang}),200


@h_route.route("/shopping-cart")
def listcart():
    try:
        menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).all()  #menu cha
        return render_template("pages/listcart.html",**locals())
    except Exception as e:
        return redirect(url_for("home.index"))
    

@h_route.route("/remove-cart",methods=['POST'])
def remove_cart():
    id = request.json.get('product_id')
    giohang=session.get('cart',{})
    if str(id) in giohang:
        del giohang[str(id)]
        session['cart']=giohang
        session.modified=True
        return jsonify({'status':'success','message':'Xóa sản phẩm thành công'}),200
    return jsonify({'status':'error','message':'Sản phẩm không tồn tại'}),400

@h_route.route('/update-cart',methods=['POST'])
def update_cart():
    product_id=request.json.get('id')
    soluong=request.json.get('sl',0)    
    nhaptay=request.json.get('nhaptay')   

    cart=session.get('cart',{})

    if str(product_id) not in cart:
        return jsonify({'success':False,"message":"Product not found"}),404
    
    sanpham=cart[str(product_id)]

    if nhaptay:
        new_quantity=max(1,soluong)
    else:
        new_quantity=max(1,sanpham['quantity']+soluong)
    #cap nhat lại so luong gio hang
    sanpham['quantity']=new_quantity

    #tổng giá mới
    productTotal=sanpham['price']*sanpham['quantity']
    cart_Total= sum(item['price']*item['quantity'] for item in cart.values())
    tongcoship=cart_Total+200000

    session['cart']=cart
    session.modified=True

    return jsonify({
        'success':True,
        'new_quantity':new_quantity,
        'productTotal':productTotal,
        'cart_Total':cart_Total,
        'tongcoship':tongcoship
    })


    
upload_folder='shop/static/uploads/'

@h_route.route('/checkout',methods=['GET','POST'])
@login_required
def checkout():
    menu_item=MenuItem.query.filter(MenuItem.parent_id.is_(None)).all()  #menu cha
    home=menu_list(menu_item)
    # Tổng tiền thanh toán
    cart=session.get('cart',{})
    total_payment= sum(item['price']*item['quantity'] for item in cart.values())
    


    user=Account.query.filter_by(id=current_user.id).first()
    form=ProfileForm(obj=user)
    if form.validate_on_submit():   
        # Cập nhật thông tin từ form
        user.fullname=form.fullname.data
        user.phone=form.phone.data
        user.address=form.address.data
        if form.password.data:
            user.password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Lưu ảnh (nếu có)
        if 'image' in request.files:
            hinhcu=user.image
            duongdan=os.path.join(upload_folder,hinhcu)
            if os.path.isfile(duongdan):
                os.remove(duongdan)
            #cập hình mới
            hinh=request.files['image'] # kích thước, tên file hinh, đuôi hinh .png...
            hinhgoc=secure_filename(hinh.filename)
            chuoi=str(int(time.time())) #thơi gian upload ảnh
            tenhinh=f'{chuoi}_{hinhgoc}' #172767233_tenhinh.png
            hinh.save(os.path.join(upload_folder,tenhinh))        
        else:
            tenhinh=user.image
        
        user.image=tenhinh 
        db.session.commit()

        # Lưu thông tin đơn hàng vào bảng order
        new_order=Order(
            user_id=current_user.id,
            total_payment=total_payment           
            )
        db.session.add(new_order)
        db.session.commit()


        # Lưu chi tiết đơn hàng vào bẳng OrderDetail
        for item in cart.values():
            new_order_detail=OrderDetail(
                order_id=new_order.id,
                product_name=item['name'],
                quantity=item['quantity'],
                price=item['price'],
                total=item['price']*item['quantity']
            )
            db.session.add(new_order_detail)

        db.session.commit()
        session.pop('cart',None)
        flash('success','Đặt hàng thành công')
        

        return redirect(url_for('home.checkout'))  
    
    return render_template("pages/checkout.html",**locals())

@h_route.route('/success')
@login_required
def success():
    return render_template("pages/success.html",**locals())

