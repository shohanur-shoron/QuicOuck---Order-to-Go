import decimal

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import update_session_auth_hash
from account.models import Profile
import Levenshtein as levenshtein
from random import shuffle
from django.contrib import messages
from account.views import index




def storeHome(request):

    user = request.user.profile

    if user.isStore == False:
        products = Product.objects.all()
        listProduct = list(products)
        shuffle(listProduct)
        catagories = Category.objects.all()
        cart = CartItem.objects.filter(user=user)
        wishList = WishList.objects.filter(user=user)
        wishListProduct = [item.product for item in wishList]
        cartProducts = [item.product for item in cart]
        cartLen = len(cartProducts)
        wishListLen = len(wishListProduct)
        context = {
            'products': products,
            'catagories': catagories,
            'cart': cart,
            'cartProducts': cartProducts,
            'cartLen': cartLen,
            'wishListLen': wishListLen,
            'wishListProduct': wishListProduct,
            'listProduct': listProduct,
        }
        return render(request, 'customerHomePage.html', context)
    else:
        user_profile = request.user.profile
        user_products = Product.objects.filter(store=user_profile)
        orders = Order.objects.filter(store=user_profile).exclude(
            status__in=['cancelled', 'picked_up']
        )
        distinct_user_ids = orders.values_list('user', flat=True).distinct()
        users = [Profile.objects.get(id=user_id) for user_id in distinct_user_ids]
        catagories = []


        for product in user_products:
            if product.category not in catagories:
                catagories.append(product.category)

        context = {
            'products': user_products,
            'catagories': catagories,
            'distinctUsers': users,
        }
        return render(request, 'vendor.html', context)

def addProductPage(request):
    catagories = Category.objects.all()
    return render(request, 'addProduct.html', {'catagories': catagories})

def addProduct(request):
    if request.method == 'POST':
        name = request.POST['Title']
        description = request.POST['prductDescription']
        price = request.POST['price']
        discountPrice = request.POST['discountPrice']
        category = request.POST['catagoryTag']
        image = request.FILES['imageUpload']
        store = request.user.profile

        if discountPrice > price:
            discountPrice = price

        catagoryObject = Category.objects.get(id=category)

        discountPersentage = get_discount_percentage(price, discountPrice)

        product = Product(name=name, description=description, price=price, discountPersentage=discountPersentage, discountPrice=discountPrice, category=catagoryObject, image=image, store=store)
        product.save()

        return redirect(storeHome)
    else:
        return render(request, 'addProduct.html')

def productPage(request):
    user_profile = request.user.profile
    user_products = Product.objects.filter(store=user_profile)
    total_products = user_products.count()

    orders = Order.objects.filter(store=user_profile).exclude(
        status__in=['cancelled', 'pending', 'ready']
    )

    totalRevenue = 0
    for order in orders:
        totalRevenue += order.product.discountPrice * order.quantity

    allOrders = Order.objects.filter(store=user_profile)
    totalOrders = allOrders.count()

    users = orders.values('user').distinct()
    totalUsers = len(users)

    context = {'products': user_products,
               'total_products': total_products,
               'totalUsers': totalUsers,
               'totalOrders': totalOrders,
               'totalRevenue': totalRevenue,
    }
    return render(request, 'product.html', context)

def get_discount_percentage(original_price, discounted_price):
    discount = int(original_price) - int(discounted_price)
    percentage = (discount / int(original_price)) * 100
    return round(percentage, 1)


def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def editProductPage(request, id):
    product = Product.objects.get(id=id)
    catagories = Category.objects.all()
    return render(request, 'editProduct.html', {'product': product, 'catagories': catagories})


def editProduct(request, id):
    product = Product.objects.get(id=id)

    name = request.POST['Title']
    description = request.POST['prductDescription']
    price = request.POST['price']
    discountPrice = request.POST['discountPrice']
    category = request.POST['catagoryTag']
    image = request.FILES.get('imageUpload', False)

    product.name = name
    product.description = description
    product.price = price
    product.discountPrice = discountPrice

    if category != 'none':
        productCategory = Category.objects.get(id=category)
        product.category = productCategory
    if image:
     product.image = image

    product.discountPersentage = get_discount_percentage(price, discountPrice)
    product.save()
    return redirect(storeHome)


def addToCart(request, id):
    product = Product.objects.get(id=id)
    user_profile = request.user.profile
    cart = CartItem(user=user_profile, product=product)
    cart.save()
    return redirect(request.META.get('HTTP_REFERER'))

def removeFromCart(request, id):
    product = Product.objects.get(id=id)
    user_profile = request.user.profile
    cart = CartItem.objects.get(user=user_profile, product=product)
    cart.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def addToWishlist(request, id):
    product = Product.objects.get(id=id)
    user_profile = request.user.profile
    cart = WishList(user=user_profile, product=product)
    cart.save()
    return redirect(request.META.get('HTTP_REFERER'))

def removeFromWishlist(request, id):
    product = Product.objects.get(id=id)
    user_profile = request.user.profile
    cart = WishList.objects.get(user=user_profile, product=product)
    cart.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def viewProduct(request, id):
    user = request.user.profile
    products = Product.objects.all()
    catagories = Category.objects.all()
    cart = CartItem.objects.filter(user=user)
    wishList = WishList.objects.filter(user=user)
    wishListProduct = [item.product for item in wishList]
    cartProducts = [item.product for item in cart]
    cartLen = len(cartProducts)
    wishListLen = len(wishListProduct)
    product = Product.objects.get(id=id)
    reviews = Review.objects.filter(product=product)
    totalReviews = reviews.count()
    context = {
        'products': products,
        'catagories': catagories,
        'cart': cart,
        'cartProducts': cartProducts,
        'cartLen': cartLen,
        'wishListLen': wishListLen,
        'wishListProduct': wishListProduct,
        'product': product,
        'reviews': reviews,
        'totalReviews': totalReviews,
    }

    return render(request, 'viewProduct.html', context)


def getStarText(num):
    if num == 0:
        return '😒'
    text = ''
    for i in range(num):
        text = text + '⭐'
    return text



def addReview(request, id):
    product = Product.objects.get(id=id)
    user = request.user
    reviewComment = request.POST['write_review']
    stars = request.POST.get('stars', 0)
    starText = getStarText(int(stars))

    product.totalReviews = product.totalReviews + 1
    if product.totalReviews > 1:
        product.avgReviewPoint = (product.avgReviewPoint + decimal.Decimal(str(stars))) / 2
    else:
        product.avgReviewPoint = product.avgReviewPoint + decimal.Decimal(str(stars))

    product.save()


    review = Review(user=user, product=product, ratingValue=stars, ratingStar=starText, comment=reviewComment)
    review.save()
    return redirect(request.META.get('HTTP_REFERER'))

def cartItem(request):
    user = request.user.profile
    products = Product.objects.all()
    catagories = Category.objects.all()
    cart = CartItem.objects.filter(user=user)
    wishList = WishList.objects.filter(user=user)
    wishListProduct = [item.product for item in wishList]
    cartProducts = [item.product for item in cart]
    cartLen = len(cartProducts)
    wishListLen = len(wishListProduct)
    context = {
        'products': products,
        'catagories': catagories,
        'carts': cart,
        'cartProducts': cartProducts,
        'cartLen': cartLen,
        'wishListLen': wishListLen,
        'wishListProduct': wishListProduct,
    }

    return render(request, 'cartItem.html', context)

def increaseCartQuantity(request, id):
    product = Product.objects.get(id=id)
    user_profile = request.user.profile
    cart = CartItem.objects.get(user=user_profile, product=product)
    cart.quantity = cart.quantity + 1
    cart.save()
    return redirect(request.META.get('HTTP_REFERER'))

def decreaseCartQuantity(request, id):
    product = Product.objects.get(id=id)
    user_profile = request.user.profile
    cart = CartItem.objects.get(user=user_profile, product=product)
    if cart.quantity > 1:
        cart.quantity = cart.quantity - 1
        cart.save()
    return redirect(request.META.get('HTTP_REFERER'))


def orderProduct(request, id):
    product = Product.objects.get(id=id)
    user_profile = request.user.profile
    pickup_time = request.POST['pickUpTime']
    store = product.store
    quantity = request.POST['quantity']

    order = Order(user=user_profile, product=product, quantity=quantity, pickup_time=pickup_time, store=store)
    order.save()

    return render(request, 'orderSuccess.html')


def orderAllCartProduct(request):
    cartItem = CartItem.objects.filter(user=request.user.profile)
    if len(cartItem) == 0:
        return redirect(storeHome)
    if request.method == 'POST':
        for i, cart in enumerate(cartItem):
            cart_id = request.POST.get(f'form-{i}-cart_id')
            if cart_id:
                time = request.POST.get(f'form-{i}-time')

                product = cart.product
                user_profile = request.user.profile
                store = product.store
                quantity = cart.quantity

                order = Order(user=user_profile, product=product, quantity=quantity, pickup_time=time, store=store)
                order.save()
                cart.delete()

    return render(request, 'orderSuccess.html')

def wishListProduct(request):
    user = request.user.profile
    products = Product.objects.all()
    catagories = Category.objects.all()
    cart = CartItem.objects.filter(user=user)
    wishList = WishList.objects.filter(user=user)
    wishListProduct = [item.product for item in wishList]
    cartProducts = [item.product for item in cart]
    cartLen = len(cartProducts)
    wishListLen = len(wishListProduct)
    context = {
        'products': products,
        'catagories': catagories,
        'cart': cart,
        'cartProducts': cartProducts,
        'cartLen': cartLen,
        'wishListLen': wishListLen,
        'wishListProduct': wishListProduct,
    }
    return render(request, 'wishListProduct.html', context)

def singleStoreProduct(request, id):
    store = Profile.objects.get(id=id)
    storeProducts = Product.objects.filter(store=store)

    user = request.user.profile
    products = Product.objects.all()
    catagories = Category.objects.all()
    cart = CartItem.objects.filter(user=user)
    wishList = WishList.objects.filter(user=user)
    wishListProduct = [item.product for item in wishList]
    cartProducts = [item.product for item in cart]
    cartLen = len(cartProducts)
    wishListLen = len(wishListProduct)
    context = {
        'products': products,
        'catagories': catagories,
        'cart': cart,
        'cartProducts': cartProducts,
        'cartLen': cartLen,
        'wishListLen': wishListLen,
        'wishListProduct': wishListProduct,
        'storeProducts': storeProducts,
        'store': store,
    }
    return render(request, 'singleStoreProduct.html', context)


def storeOrder(request):
    store = request.user.profile
    orders = Order.objects.filter(store=store).exclude(
        status__in=['cancelled', 'picked_up']
    )

    users = orders.values('user').distinct()

    orderList = []
    totalBill = []

    for user_dict in users:
        user = user_dict['user']  # Get the Profile object from the dictionary
        userOrder = Order.objects.filter(user=user, store=store).exclude(
        status__in=['cancelled', 'picked_up']
        )
        orderList.append(userOrder)

    for orders in orderList:
        totalCost = 0
        for order in orders:
            totalCost += order.product.discountPrice * order.quantity
        totalBill.append(totalCost)

    zipped = zip(totalBill, orderList)

    context = {
        'orderList': orderList,
        'users': users,
        'zipped': zipped,
    }

    return render(request, 'storeOrder.html', context)


def orderStatusToReady(request, id):
    store = request.user.profile
    user = Profile.objects.get(id=id)

    userOrder = Order.objects.filter(user=user, store=store)

    for order in userOrder:
        if order.status == 'pending':
            order.status = 'ready'
            order.save()

    return redirect(request.META.get('HTTP_REFERER'))

def viewOrderCancelpage(request, id):
    return render(request, 'cancelOrder.html',{'ID': id})

def viewOrderCancelpageForIndivisualProduct(request, id):
    return render(request, 'cancelOrderIndivusual.html',{'ID': id})

def orderStatusToCancel(request, id):
    store = request.user.profile
    user = Profile.objects.get(id=id)
    reason = request.POST.get('reason')

    userOrder = Order.objects.filter(user=user, store=store)

    for order in userOrder:
        order.status = 'cancelled'
        order.cancelReason = reason
        order.save()

    return redirect(storeOrder)

def orderStatusToPickedUp(request, id):
    store = request.user.profile
    user = Profile.objects.get(id=id)

    userOrder = Order.objects.filter(user=user, store=store)

    for order in userOrder:
        if order.status == 'ready':
            order.status = 'picked_up'
            order.save()

    return redirect(request.META.get('HTTP_REFERER'))


def customerOrderView(request):
    user = request.user.profile

    orders = Order.objects.filter(user=user).exclude(
        status__in=['cancelled', 'picked_up']
    )

    catagories = Category.objects.all()
    cart = CartItem.objects.filter(user=user)
    wishList = WishList.objects.filter(user=user)
    wishListProduct = [item.product for item in wishList]
    cartProducts = [item.product for item in cart]
    cartLen = len(cartProducts)
    wishListLen = len(wishListProduct)
    context = {
        'catagories': catagories,
        'cart': cart,
        'cartProducts': cartProducts,
        'cartLen': cartLen,
        'wishListLen': wishListLen,
        'wishListProduct': wishListProduct,
        'orders': orders,
    }

    return render(request, 'customerOrderView.html', context)

def customerOrderHistoryView(request):
    user = request.user.profile

    orders = Order.objects.filter(user=user).exclude(
        status__in=['pending', 'ready']
    )

    catagories = Category.objects.all()
    cart = CartItem.objects.filter(user=user)
    wishList = WishList.objects.filter(user=user)
    wishListProduct = [item.product for item in wishList]
    cartProducts = [item.product for item in cart]
    cartLen = len(cartProducts)
    wishListLen = len(wishListProduct)
    context = {
        'catagories': catagories,
        'cart': cart,
        'cartProducts': cartProducts,
        'cartLen': cartLen,
        'wishListLen': wishListLen,
        'wishListProduct': wishListProduct,
        'orders': orders,
    }

    return render(request, 'customerOrderView.html', context)

def discountedProducts(request):
    user = request.user.profile
    discounted_products = Product.objects.filter(~Q(discountPersentage=0.0)).order_by('-discountPersentage')

    catagories = Category.objects.all()
    cart = CartItem.objects.filter(user=user)
    wishList = WishList.objects.filter(user=user)
    wishListProduct = [item.product for item in wishList]
    cartProducts = [item.product for item in cart]
    cartLen = len(cartProducts)
    wishListLen = len(wishListProduct)
    context = {
        'catagories': catagories,
        'cart': cart,
        'cartProducts': cartProducts,
        'cartLen': cartLen,
        'wishListLen': wishListLen,
        'wishListProduct': wishListProduct,
        'products': discounted_products,
    }

    return render(request, 'discountProduct.html', context)

def categoryProducts(request, id):
    category = Category.objects.get(id=id)
    products = category.products.all()

    user = request.user.profile
    catagories = Category.objects.all()
    cart = CartItem.objects.filter(user=user)
    wishList = WishList.objects.filter(user=user)
    wishListProduct = [item.product for item in wishList]
    cartProducts = [item.product for item in cart]
    cartLen = len(cartProducts)
    wishListLen = len(wishListProduct)
    context = {
        'catagories': catagories,
        'cart': cart,
        'cartProducts': cartProducts,
        'cartLen': cartLen,
        'wishListLen': wishListLen,
        'wishListProduct': wishListProduct,
        'storeProducts': products,
        'category': category,
    }

    return render(request, 'catagoryStoreProduct.html', context)



def makeStatusToPickedUp(request, id):
    order = Order.objects.get(id=id)
    order.status = 'picked_up'
    order.save()
    return redirect(request.META.get('HTTP_REFERER'))

def makeStatusToPending(request, id):
    order = Order.objects.get(id=id)
    order.status = 'pending'
    order.save()
    return redirect(request.META.get('HTTP_REFERER'))

def makeStatusToReady(request, id):
    order = Order.objects.get(id=id)
    order.status = 'ready'
    order.save()
    return redirect(request.META.get('HTTP_REFERER'))

def makeStatusToCancle(request, id):
    order = Order.objects.get(id=id)
    order.status = 'cancelled'
    order.cancelReason = request.POST.get('cancleReason')
    order.save()
    return redirect(storeOrder)


def storeOrderHistory(request):
    store = request.user.profile
    orders = Order.objects.filter(store=store).exclude(
        status__in=['pending', 'ready']
    )

    users = orders.values('user').distinct()

    orderList = []
    totalBill = []

    for user_dict in users:
        user = user_dict['user']  # Get the Profile object from the dictionary
        userOrder = Order.objects.filter(user=user, store=store).exclude(
            status__in=['pending', 'ready']
        )
        orderList.append(userOrder)

    for orders in orderList:
        totalCost = 0
        for order in orders:
            totalCost += order.product.discountPrice * order.quantity
        totalBill.append(totalCost)

    zipped = zip(totalBill, orderList)

    context = {
        'orderList': orderList,
        'users': users,
        'zipped': zipped,
    }

    return render(request, 'storeOrderHistory.html', context)



def searchProducts(request):
    if request.method == 'POST':
        search_text = request.POST.get('searchText', '').strip()

        # Basic search (case-insensitive)
        products = Product.objects.filter(
            Q(name__icontains=search_text) |
            Q(description__icontains=search_text)
        )

        # Advanced search (handles spelling mistakes using Levenshtein distance)
        advanced_search_products = []
        for product in Product.objects.all():
            name_distance = levenshtein.distance(product.name.lower(), search_text.lower())
            description_distance = levenshtein.distance(product.description.lower(), search_text.lower())
            if name_distance <= 3 or description_distance <= 3:
                advanced_search_products.append(product)


        # Combine the results from basic and advanced search
        all_products = list(set(products) | set(advanced_search_products))

        user = request.user.profile
        products = Product.objects.all()
        catagories = Category.objects.all()
        cart = CartItem.objects.filter(user=user)
        wishList = WishList.objects.filter(user=user)
        wishListProduct = [item.product for item in wishList]
        cartProducts = [item.product for item in cart]
        cartLen = len(cartProducts)
        wishListLen = len(wishListProduct)
        context = {
            'products': products,
            'catagories': catagories,
            'cart': cart,
            'cartProducts': cartProducts,
            'cartLen': cartLen,
            'wishListLen': wishListLen,
            'wishListProduct': wishListProduct,
            'searchProducts': all_products,
            'search_text': search_text,
        }
        return render(request, 'search_results.html', context)

    return redirect(storeHome)


def allTheStore(request):
    user = request.user.profile
    catagories = Category.objects.all()
    cart = CartItem.objects.filter(user=user)
    wishList = WishList.objects.filter(user=user)
    wishListProduct = [item.product for item in wishList]
    cartProducts = [item.product for item in cart]
    cartLen = len(cartProducts)
    wishListLen = len(wishListProduct)

    allStore = Profile.objects.filter(isStore=True)

    context = {
        'cartLen': cartLen,
        'wishListLen': wishListLen,
        'allStore': allStore,
        'catagories': catagories,
    }

    return render(request, 'allTheStoreView.html', context)

def uniquePhoneNumber(phoneNumber):
    try:
        Profile.objects.get(phone=phoneNumber)
        return False
    except Profile.DoesNotExist:
        return True

def editProfilePage(request, id):
    editProfile = Profile.objects.get(id=id)
    return render(request, 'editProfile.html', {'editProfile': editProfile})

def editProfile(request, id):
    editProfile = Profile.objects.get(id=id)
    phone = request.POST.get('phone')
    if phone != editProfile.phone:
        if uniquePhoneNumber(phone):
            editProfile.phone = phone
            editProfile.save()
        else:
            message1 = 'Account already exists with this Phone Number! Please use a different one.'
            messages.info(request, message1)
            return redirect('editProfilePage', id=id)

    fname = request.POST.get('firstName')
    lname = request.POST.get('lastName')
    email = request.POST.get('email')
    image = request.FILES.get('imageUpload')
    if editProfile.isStore:
        storeName = request.POST.get('storeName')
        if storeName != editProfile.storeName and storeName != "":
            editProfile.storeName = storeName
            editProfile.save()

    if fname != '' and lname != '' and email != '':
        if fname != editProfile.user.first_name:
            editProfile.user.first_name = fname
            editProfile.user.save()
        if lname != editProfile.user.last_name:
            editProfile.user.last_name = lname
            editProfile.user.save()
        if email != editProfile.user.email:
            editProfile.user.email = email
            editProfile.user.save()

    if image:
        editProfile.image = image
        editProfile.save()

    return redirect('storeHome')

def changePasswordPage(request, id):
    editProfile = Profile.objects.get(id=id)
    return render(request, 'changePassword.html', {'editProfile': editProfile})

def changePassword(request, id):
    editProfile = Profile.objects.get(id=id)
    oldPassword = request.POST.get('oldPassword')
    newPassword = request.POST.get('newPassword')
    confirmPassword = request.POST.get('confNewPassword')

    if editProfile.user.check_password(oldPassword):
        if newPassword == confirmPassword:
            editProfile.user.set_password(newPassword)
            editProfile.user.save()
            update_session_auth_hash(request, editProfile.user)
            return redirect(index)
        else:
            message1 = 'Password mismatch! Please try again.'
            messages.info(request, message1)
            return redirect('changePasswordPage', id=id)
    else:
        message1 = 'Wrong password. Please try again.'
        messages.info(request, message1)
        return redirect('changePasswordPage', id=id)