# Setninel-5p_tools

Python API to quarry and download Sentinel 5P data products.

### Request data products for last X days and get short response

.. code-block::

    from download import s5_quarry
    
        # Returns json with products list formated as: {'identifier','uuid','date'}
    data = s5_quarry(days=10)
   
### Download latest product by uuid

.. code-block::

    data = s5_quarry(days=10)
    
    #Getting first product 'uuid' from the list of products
    first_product_uuid =  data[0]['uuid']
    #Downloading product
    download_product(uuid,'C:\\Users\\Computer\\')
   
### Request specific products for last X days and get short response

.. code-block::
    
    data = s5_quarry(days=10, product_type=FORMALDEHYDE)

### Request specific products FROM date xx-xx-xxxx TO xx-xx-xxxx and get short response

.. code-block::

    data = s5_quarry(days=10, product_type=FORMALDEHYDE,ingestion_date_FROM='2019-06-17', ingestion_date_TO='2019-07-17')

### Request specific products for last X days, intersecting WKT geometry and get short response

.. code-block::
    
    boundary = 'POLYGON((29.455470185302943 60.155370540303764,31.064967255615443 60.155370540303764,31.064967255615443 59.67348573740844,29.455470185302943 59.67348573740844,29.455470185302943 60.155370540303764))'
    quarry = s5_quarry(days=10, product_type=FORMALDEHYDE,wkt=boundary)



### Request data products for last X days and get full response   

.. code-block::

    data = quarry = s5_quarry(days=10,full_response=True)
    # Returns json with products formated as s5phub response
