from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from helpers.cpf import validate_CPF
from helpers.barcode import validate_ean
import hashlib
from pagseguro import PagSeguro
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Username', max_length=128, unique=True)
    email = models.EmailField('Email', unique=True, max_length=128, validators=[validators.EmailValidator])
    cpf = models.CharField('Cpf', max_length=11, unique=True, validators=[validate_CPF])
    func_smarket_active = models.BooleanField('Smarket', default=False)
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    date_joined = models.DateTimeField('Data de entrada', auto_now_add=True)

    class Meta:
        verbose_name = 'Usuario'

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'cpf']
    objects = UserManager()

    def get_name(self):
        return str(self.username)

    def get_short_name(self):
        return str(self.username).split(" ")[0]

class Product(models.Model):
    name = models.CharField('Nome', max_length=128, unique=True)
    weight = models.FloatField('Peso', max_length=8)
    price = models.FloatField('Preco', max_length=8)
    image = models.ImageField(upload_to='images')
    bar_code = models.CharField('Cod_barras', max_length=13, validators=[validate_ean])
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Produto'

class Purchase(models.Model):
    id_user = models.ForeignKey('User', verbose_name='Usuário')
    id_validator = models.ForeignKey('Validator', verbose_name='Validação')
    value = models.FloatField('Valor', max_length=8)
    transaction_code = models.CharField('Código de Transação', max_length=13)
    created_at = models.DateTimeField(auto_now_add=True)
    products_name = models.ForeignKey('Product', verbose_name='Produto')
    class Meta:
        verbose_name = 'Compra'


    def pagseguro(self, email, user):
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, 
            token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
            )
        pg.sender = {
            'email': email
        }
        pg.reference_prefix = None
        pg.shipping = None
        pg.reference = self.pk
        cart = Cart.objects.filter(id_user= user).values('id')
        itens = Item.objects.filter(id_cart= cart)
        print(itens.values())
        for item in itens:
            obj = Product.objects.filter(id=item.id_product_id).values('price')
            price = obj[0].get('price')
            #print (Product.objects.filter(id=item.id_product_id).values(*'price'))
            pg.items.append(
                {
                    'id': item.id_product_id,
                    'description': Product.objects.filter(id=item.id_product_id).values('name'),#item.id_product_name,
                    'quantity': item.quantity,
                    'amount': '%.2f' % price
                }
                )
        return pg
                

class Item(models.Model):
    id_product = models.ForeignKey('Product', verbose_name='Produto')
    id_cart = models.ForeignKey('Cart', verbose_name='Carrinho')
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Itens'

    def __str__(self):
        return "{} unidade(s) de {}".format(self.quantity, self.id_product.name)

class Cart(models.Model):
    id_user = models.ForeignKey('User', verbose_name='Usuário')
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    finalized = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Carrinho'

    def __str__(self):
        return "{} - {}".format(self.id_user.username, self.pk)

    def gerarhash(self):
        h = hashlib.md5()
        h.update(self.pk)
        return "{} - {}".format(self.h.hexdigest())

class Validator(models.Model):
    id_cart = models.ForeignKey('Cart', verbose_name='Carrinho')
    ok = models.BooleanField(default=False)
    report = models.CharField('Relatório', max_length=13)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    class Meta:
        verbose_name = 'Validação'
        verbose_name_plural = 'Validações'

#class ChangePass(models.Model):
#    id_user = models.ForeignKey('User', verbose_name='Usuario')
#    key = models.CharField('key', verbose_name ='Key')
#    expira = models.DateTimeField


class OrderManager(models.Manager):

    def create_order(self, user):
        order = self.create(user=user)
        
            
        return order





class Order(models.Model):

    

    STATUS_CHOICES = (
        (0, 'Aguardando Pagamento'),
        (1, 'Concluída'),
        (2, 'Cancelada'),
    )

    PAYMENT_OPTION_CHOICES = (
        ('deposit', 'Depósito'),
        ('pagseguro', 'PagSeguro'),
        ('paypal', 'Paypal'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário')
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=0, blank=True
    )
    payment_option = models.CharField(
        'Opção de Pagamento', choices=PAYMENT_OPTION_CHOICES, max_length=20,
        default='deposit'
    )

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    objects = OrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return 'Pedido #{}'.format(self.pk)


    def total(self):
        
        cart = Cart.objects.filter(id_user= self.user).values('id')
        itens = Item.objects.filter(id_cart= cart)
        print(itens.values())
        count = 0
        for item in itens:
            obj = Product.objects.filter(id=item.id_product_id).values('price')
            price = obj[0].get('price')
            quantity = item.quantity
            count = count + (price * quantity)
        
        return count

    def pagseguro_update_status(self, status):
        if status == '3':
            self.status = 1
        elif status == '7':
            self.status = 2
        self.save()

    def complete(self):
        self.status = 1
        self.save()

    

    def pagseguro(self, email, user):
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, 
            token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
            )
        pg.sender = {
            'email': email
        }
        pg.reference_prefix = None
        pg.shipping = None
        pg.reference = self.pk
        cart = Cart.objects.filter(id_user= user).values('id')
        itens = Item.objects.filter(id_cart= cart)
        print('EM BAIXO!!!')
        print(Product.objects.filter(id=item.id_product_id).values('name')[0].get('name'))
        for item in itens:
            obj = Product.objects.filter(id=item.id_product_id).values('price')
            price = obj[0].get('price')
            obj2 = Product.objects.filter(id=item.id_product_id).values('name')
            name = obj2[0].get('name')

            #print (Product.objects.filter(id=item.id_product_id).values(*'price'))
            pg.items.append(
                {
                    'id': item.id_product_id,
                    'description': name,
                    'quantity': item.quantity,
                    'amount': '%.2f' % price
                }
                )
        
        return pg