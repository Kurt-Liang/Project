# Generated by Django 2.2.1 on 2019-05-18 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='類型標題')),
                ('picture', models.ImageField(null=True, upload_to='static/upload/goodstype', verbose_name='類型圖片')),
                ('desc', models.TextField(verbose_name='類型描述')),
            ],
            options={
                'verbose_name': '商品類型',
                'verbose_name_plural': '商品類型',
                'db_table': 'goods_type',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='商品名稱')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='商品價格')),
                ('spec', models.CharField(max_length=20, verbose_name='商品規格')),
                ('picture', models.ImageField(null=True, upload_to='static/upload/goods', verbose_name='商品圖片')),
                ('isActive', models.BooleanField(default=True, verbose_name='是否上架')),
                ('goodsType', models.ForeignKey(on_delete='CASCADE', to='index.GoodsType', verbose_name='商品類型')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'db_table': 'goods',
            },
        ),
    ]
