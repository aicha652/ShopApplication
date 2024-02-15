# Define all the routes
from flask import send_from_directory, render_template, url_for, flash, redirect, request, jsonify, abort, current_app, session
from Ecommerce.models import User, Product, Order, Cart
from Ecommerce.forms import LoginForm, UserForm, AddProducts, EditUserForm
from Ecommerce import app, db, bcrypt, photos
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os, secrets
from flask_mail import Message


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    return render_template('home.html')


@app.route('/about', strict_slashes=False)
def about():
    return render_template('about.html')

@app.route('/all_products', strict_slashes=False)
def all_products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page)
    return render_template('all_products.html', title="Store Home", products=products)


@app.route('/signup', methods=["POST", "GET"])
def signup():
    form  = UserForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data,
                password=hash_password, country=form.country.data,
                address=form.address.data, phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome:{form.username.data} Thank Your for Registering", 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            if user.is_admin:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check your credentials and try again')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/logoutAdmin')
def logoutAdmin():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        count_users = User.query.count()
        count_products = Product.query.count()
        return render_template('dashboard.html', count_users=count_users, count_products=count_products)


@app.route('/addproduct', methods=["GET", "POST"])
def addproduct():
    form = AddProducts()
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        desc = form.desc.data
        image_1 = photos.save(request.files['image_1'] , name=secrets.token_hex(10) + '.')
        print(f"Image 1 name:{image_1}, its type:{type(image_1)}")
        product = Product(name=name, price=price, desc=desc, 
        image_1=image_1)
        db.session.add(product)
        flash(f"{name} has been added to database.", 'success')
        db.session.commit()
        return redirect(url_for('products'))
    return render_template('add_product.html', form=form)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/deleteuser/<int:id>', methods=["POST"])
def deleteuser(id):
    user = User.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        flash(f'{user.username} Deleted', 'success')
        return redirect(url_for('users'))
    flash(f'Cant delete {user.username}', 'warning')
    return redirect(url_for('users'))


@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)


@app.route('/deleteproduct/<int:id>', methods=["POST"])
def deleteproduct(id):
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
            except Exception as e:
                print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'{product.name} Deleted', 'success')
        return redirect(url_for('products'))
    flash(f'Cant delete {product.name}', 'warning')
    return redirect(url_for('products'))


@app.route('/updateproduct/<int:id>', methods=["GET", "POST"])
def updateproduct(id):
    product = Product.query.get_or_404(id)
    form = AddProducts(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.desc = form.desc.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
                product.image_1 = photos.save(request.files['image_1'] , name=secrets.token_hex(10) + '.')
            except:
                product.image_1 = photos.save(request.files['image_1'] , name=secrets.token_hex(10) + '.')
        db.session.commit()
        flash('Product Updated', 'success')
        return redirect(url_for('products'))
    form.name.data = product.name
    form.price.data = product.price
    form.desc.data = product.desc
    return render_template('update_product.html', form=form,product=product)


@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product, title=product.name)




@app.route("/addcart", methods=["POST"])
def addcart():
    if current_user.is_authenticated:
        if request.method == 'POST':
            product_id = int(request.form.get('product_id'))
            quantity = int(request.form.get('quantity'))

            # Create a Cart object with the current user, the selected product, and the specified quantity
            cart_item = Cart(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )

            # Add the cart item to the database
            db.session.add(cart_item)
            db.session.commit()

            flash(f'{quantity} item(s) successfully added to cart!', 'success')
            return redirect(url_for('cart'))
    else:
        flash('Please log in to add items to the cart.', 'danger')
        return redirect(url_for('login'))
    

@app.route("/cart")
def cart():
    if current_user.is_authenticated:
        # Assuming you have a Cart model with a quantity field
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        # Create a dictionary to store aggregated quantities by product_id
        aggregated_cart = {}
        for item in cart_items:
            if item.product_id not in aggregated_cart:
                # If the product_id is not in the dictionary, add it with the quantity
                aggregated_cart[item.product_id] = item.quantity
            else:
                # If the product_id is already in the dictionary, increment the quantity
                aggregated_cart[item.product_id] += item.quantity

        # Retrieve the actual Product objects for the products in the cart
        products_in_cart = Product.query.filter(Product.id.in_(aggregated_cart.keys())).all()

        # Combine the product information with the aggregated quantities
        cart_info = [{"product": product, "quantity": aggregated_cart[product.id]} for product in products_in_cart]

        total_value = sum(item['product'].price * item['quantity'] for item in cart_info)

        # Calculate total_quantity (total number of all products)
        total_quantity = sum(item['quantity'] for item in cart_info)
        return render_template("cart.html", cart_info=cart_info, total_value=total_value, total_quantity=total_quantity)
    else:
        flash('Please log in to view your cart.', 'danger')
        return redirect(url_for('login'))   

@app.route('/cart/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    quantity = int(request.form['quantity'])
    # Update the cart item in the database
    cart_item = Cart.query.filter_by(product_id=item_id).first()
    if cart_item.quantity:
        cart_item.quantity += 1
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/cart/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    # Delete the cart item from the database
    cart_item = Cart.query.filter_by(product_id=item_id).first()
    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/profile')
def profile():
    user = User.query.get_or_404(current_user.id)
    form = EditUserForm(obj=user)
    return render_template('profile.html', form=form, user=user)

@app.route('/updateprofile/<int:id>', methods=["GET", "POST"])
def updateprofile(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(request.form)
    if request.method == "POST":
        user.username = form.username.data
        user.email = form.email.data
        user.country = form.country.data
        user.address = form.address.data
        user.phone = form.phone.data
        db.session.commit()
        flash('Profile Updated', 'success')
        return redirect(url_for('profile'))
    form.username.data = user.username
    form.email.data = user.email
    form.country.data = user.country
    form.address.data = user.address
    form.phone.data = user.phone
    return render_template('profile.html', form=form, user=user)




@app.route('/account')
def account():
    user = User.query.get_or_404(current_user.id)
    form = EditUserForm(obj=user)
    return render_template('account.html', form=form, user=user)

@app.route('/updateaccount/<int:id>', methods=["GET", "POST"])
def updateaccount(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(request.form)
    if request.method == "POST":
        user.username = form.username.data
        user.email = form.email.data
        user.country = form.country.data
        user.address = form.address.data
        user.phone = form.phone.data
        db.session.commit()
        flash('Profile Updated', 'success')
        return redirect(url_for('users'))
    form.username.data = user.username
    form.email.data = user.email
    form.country.data = user.country
    form.address.data = user.address
    form.phone.data = user.phone
    return render_template('account.html', form=form, user=user)