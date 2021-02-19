To use this module, you need to:

#. Go to the product page.
<<<<<<< HEAD
#. In the general tab, there's a list called *Other Prices*.
#. You can add one for every price name available.
=======
#. In the general tab, there's a list called *Prices*.
#. You can add one for every multiple price field name available.
>>>>>>> [ADD] product_multi_price: New Module

To base pricelist rules on that fields, in the pricelist:

#. Add a rule and choose *formula* as the computing method.
<<<<<<< HEAD
#. In the *Based on* dropdown list, select *Other Price*.
#. A new list appear: *Other Price Name*. Pick the one you need.
=======
#. In the *Based on* dropdown list you can select *Multiple Prices*.
#. A new list appear: *Multiple Price Field Name*. Pick the one you need.
>>>>>>> [ADD] product_multi_price: New Module
#. Configure the formula.
#. Now the rule is based on that price for the products that have it
   configured. Otherwise, it will return 0.
