from __future__ import absolute_import
from decimal import Decimal

import pytest
from mock import patch
from django.db import models

from easymoney import MoneyField
from .models import Product, Game, GameMoney


pytestmark = pytest.mark.django_db


def test_save():
    p = Product()
    p.price = 3.14
    p.save()


def test_get():
    p = Product.objects.create(price=3.14)

    p2 = Product.objects.get(pk=p.pk)
    assert p2.price == p.price

    # coercing
    p2 = Product.objects.get(price=3.136)
    assert p2.pk == p.pk


def test_fetch():
    Product.objects.bulk_create([
        Product(price=2.78),
        Product(price=3.14),
        Product(price=3.78),
    ])

    assert list(Product.objects.filter(price__lt=3.5).values_list('price', flat=True)) \
        == [Decimal('2.78'), Decimal('3.14')]


def test_places():
    with patch('easymoney.Money.DECIMAL_PLACES', 3):
        class Round(models.Model):
            bet = MoneyField()

        assert Round._meta.get_field('bet').decimal_places == 3


def test_subclass():
    g = Game.objects.create(prize=15)
    assert isinstance(g.prize, GameMoney)

    g2 = Game.objects.get(pk=g.pk)
    assert isinstance(g2.prize, GameMoney)
    assert g2.prize == g.prize
