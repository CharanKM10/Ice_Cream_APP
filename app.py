from flask import Flask, render_template, request, redirect, url_for, session
from database import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def home():
    search_query = request.form.get('search_query', '').strip()


    if search_query:
        seasonal_flavors = search_flavors(search_query)
    else:
        seasonal_flavors = get_seasonal_flavors()


    cart_items = get_user_cart(session.get('user_id', 1))


    if request.method == 'POST' and 'allergen_name' in request.form:
        allergen_name = request.form['allergen_name'].strip()
        if allergen_name and not allergen_exists(allergen_name):
            add_allergen(allergen_name)


    if request.method == 'POST' and 'suggestion' in request.form:
        suggestion_text = request.form['suggestion'].strip()
        if suggestion_text:
            add_customer_suggestion(suggestion_text)

    return render_template('home.html', flavors=seasonal_flavors, cart=cart_items)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'flavor_name' in request.form:
            add_flavor(
                request.form['flavor_name'],
                request.form['description'],
                'available' in request.form,
                int(request.form['quantity'])
            )
        elif 'ingredient_name' in request.form:
            add_ingredient(request.form['ingredient_name'])
        elif 'allergen_name' in request.form:
            add_allergen(request.form['allergen_name'])

    return render_template(
        'admin.html',
        flavors=get_seasonal_flavors(),
        ingredients=get_ingredients(),
        allergens=get_allergens(),
        suggestions=get_customer_suggestions()
    )

@app.route('/admin/delete_flavor/<int:flavor_id>', methods=['POST'])
def delete_flavor(flavor_id):
    delete_flavor_by_id(flavor_id)
    return redirect(url_for('admin'))

@app.route('/add_to_cart/<int:flavor_id>', methods=['POST'])
def add_to_cart_route(flavor_id):
    user_id = session.get('user_id', 1)
    add_to_cart(user_id, flavor_id, 1)
    return redirect(url_for('home'))

@app.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
def remove_from_cart_route(cart_item_id):
    user_id = session.get('user_id', 1)
    cart_item = get_cart_item_by_id(cart_item_id)

    if cart_item:
        remove_from_cart(user_id, cart_item_id, cart_item['quantity'])
        update_flavor_quantity(cart_item['flavor_id'], cart_item['quantity'])

    return redirect(url_for('home'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)