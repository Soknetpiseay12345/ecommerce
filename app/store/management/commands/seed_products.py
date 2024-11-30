from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Seed the products table with predefined skincare products data'

    def handle(self, *args, **kwargs):
        # Clear existing products for clean seeding (optional)
        Product.objects.all().delete()

        # Predefined skincare products
        products = [
            {"name": "Neutrogena Hydro Boost Water Gel", "description": "A lightweight gel moisturizer with hyaluronic acid.", "price": 19.99, "stock": 50, "image_url": "https://ntg-catalog.imgix.net/products/6811047-202307-carousel-1-2.webp?fm=jpg&auto=format&w=1200&h=1443&fit=crop"},
            {"name": "CeraVe Hydrating Facial Cleanser", "description": "A gentle, non-foaming cleanser for normal to dry skin.", "price": 14.99, "stock": 75, "image_url": "https://assets-cdn.vtenh.com/rails/active_storage/representations/proxy/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBeURGQ1E9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--4459bfa5acb44298d2c0b03b62e499d37739555c/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaDdCem9MWm05eWJXRjBTU0lJYW5CbkJqb0dSVlE2RTNKbGMybDZaVjloYm1SZmNHRmtXd2RwQWxnQ2FRSllBZz09IiwiZXhwIjpudWxsLCJwdXIiOiJ2YXJpYXRpb24ifX0=--3dee1ed9b6e56500806820ced664e44d84074fae/CeraVe%20Hydrating%20Facial%20Cleanser%2087ml%20for%20Normal%20to%20Dry%20Skin.jpg?locale=en"},
            {"name": "Olay Regenerist Micro-Sculpting Cream", "description": "Anti-aging cream that helps visibly reduce fine lines and wrinkles.", "price": 24.99, "stock": 40, "image_url": "https://m.media-amazon.com/images/I/618oOueNVHL._SL1500_.jpg"},
            {"name": "The Ordinary Niacinamide 10% + Zinc 1%", "description": "A serum designed to target blemishes, congestion, and sebum production.", "price": 6.99, "stock": 100, "image_url": "https://i5.walmartimages.com/seo/The-Ordinary-Niacinamide-10-Zinc-1-High-Strength-Vitamin-and-Mineral-Blemish-Formula-30ml_a12337ed-4b89-48b2-8dd0-e69b1eecb625.71104854b4cfdafc3c56a544c1ab9ee4.jpeg"},
            {"name": "Drunk Elephant T.L.C. Sukari Babyfacial", "description": "An AHA/BHA mask that exfoliates to reveal smoother, brighter skin.", "price": 80.00, "stock": 30, "image_url": "https://www.glowgirl.net/hs-fs/hubfs/babyfacial.jpg?width=375&name=babyfacial.jpg"},
            {"name": "CeraVe AM Facial Moisturizing Lotion SPF 30", "description": "Moisturizer with broad-spectrum SPF 30 for daily protection.", "price": 18.99, "stock": 60, "image_url": "https://www.cerave.com/-/media/project/loreal/brand-sites/cerave/americas/us/products/am-facial-moisturizing-lotion/desktop/lor2384_am30_front_700x785-(002).jpg?rev=bd764d6269704564ab030d1959ce7d5d&w=500&hash=599C9D3FC32ECC9C84CCCAF26D9929F8"},
            {"name": "La Roche-Posay Anthelios Melt-in Sunscreen Milk SPF 60", "description": "A sunscreen offering broad-spectrum protection and a non-greasy finish.", "price": 36.00, "stock": 45, "image_url": "https://img.lazcdn.com/g/p/dacf91f3c9a7f17f8f53d911950a25d4.jpg_720x720q80.jpg_.webp"},
            {"name": "Clinique Moisture Surge 72-Hour Auto-Replenishing Hydrator", "description": "Oil-free, gel-cream for instant moisture.", "price": 39.50, "stock": 80, "image_url": "https://cdn.cosmostore.org/cache/front/shop/products/625/1928502/650x650.jpg"},
            {"name": "Tatcha The Dewy Skin Cream", "description": "A rich, dewy moisturizer that promotes a glowing, hydrated complexion.", "price": 68.00, "stock": 25, "image_url": "https://s.cdnsbn.com/images/products/l/27960882401-2.jpg"},
            {"name": "Kiehl’s Calendula Herbal Extract Alcohol-Free Toner", "description": "A soothing toner that helps reduce redness and inflammation.", "price": 45.00, "stock": 70, "image_url": "https://www.kiehls.com/dw/image/v2/AAFM_PRD/on/demandware.static/-/Sites-kiehls-master-catalog/default/dw10515201/nextgen/other/bundles/KU-8909-cal-toner_ccdss-Affiliate-Duos-2400x2400.jpg?sw=320&sh=320&sm=cut&sfrm=jpg&q=70"},
            {"name": "L’Oréal Paris Revitalift Bright Reveal Brightening Peel Pads", "description": "Exfoliating pads with glycolic acid to improve skin texture and radiance.", "price": 17.99, "stock": 120, "image_url": "https://dr9wvh6oz7mzp.cloudfront.net/i/1326001de1a6f420d4340489be63d959_ra,w380,h380_pa,w380,h380.jpg"},
            {"name": "Neutrogena Ultra Sheer Dry-Touch Sunscreen SPF 100+", "description": "High SPF sunscreen that provides broad-spectrum protection.", "price": 8.99, "stock": 150, "image_url": "https://ntg-catalog.imgix.net/products/6811276_MAIN.jpg?fm=jpg&auto=format&w=1200&h=1443&fit=crop"},
            {"name": "The Ordinary Hyaluronic Acid 2% + B5", "description": "A hydrating serum that delivers moisture to the skin.", "price": 6.80, "stock": 110, "image_url": "https://assets-cdn.vtenh.com/rails/active_storage/representations/proxy/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBM2RYQ1E9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--1747d579227d4fe48203b18220134dafe6b58406/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaDdCem9MWm05eWJXRjBTU0lJYW5CbkJqb0dSVlE2RTNKbGMybDZaVjloYm1SZmNHRmtXd2RwQWxnQ2FRSllBZz09IiwiZXhwIjpudWxsLCJwdXIiOiJ2YXJpYXRpb24ifX0=--3dee1ed9b6e56500806820ced664e44d84074fae/515yLd5iR9L.jpg?locale=en"},
            {"name": "Tata Harper Clarifying Cleanser", "description": "A clarifying cleanser that helps reduce oil and prevent acne.", "price": 58.00, "stock": 30, "image_url": "https://bluemercury.com/cdn/shop/files/global_images-813269021705-1_9a380b7d-d7df-4460-a212-6cdce38be351.jpg?v=1725065108&width=600"},\
            {"name": "Fresh Rose Face Mask", "description": "Hydrating and soothing mask infused with real rose petals.", "price": 62.00, "stock": 20, "image_url": "https://www.fresh.com/dw/image/v2/BDJQ_PRD/on/demandware.static/-/Sites-fresh_master_catalog/default/dw9c234c24/product_images/H00006352_primary.jpg?sw=1350&sh=900&bgcolor=F7F7F8&sfrm=jpg"},
            {"name": "Drunk Elephant C-Firma Day Serum", "description": "A potent vitamin C serum that fights signs of aging.", "price": 78.00, "stock": 30, "image_url": "https://static.thcdn.com/productimg/original/13310315-4075177669522793.jpg"},
            {"name": "Biossance Squalane + Vitamin C Rose Oil", "description": "A nourishing oil that brightens and hydrates the skin.", "price": 72.00, "stock": 40, "image_url": "https://static.thcdn.com/productimg/original/12766621-1785143164103950.jpg"},
            {"name": "Murad AHA/BHA Exfoliating Cleanser", "description": "A dual-action exfoliating cleanser with AHA and BHA.", "price": 40.00, "stock": 60, "image_url": "https://www.murad.com.au/cdn/shop/files/AHA_BHA_Exfoliating_Cleanser_Carousel_1_MURAD.png?v=1725253994"},
            {"name": "Olay Luminous Tone Perfecting Cream", "description": "Moisturizer designed to brighten and even out skin tone.", "price": 28.00, "stock": 50, "image_url": "https://cdn.cosmostore.org/cache/front/shop/products/143/348202/650x650.jpg"},
            
        ]

        # Create each predefined product
        for product in products:
            Product.objects.create(
                name=product['name'],
                description=product['description'],
                price=product['price'],
                stock=product['stock'],
                image_url=product['image_url']
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded skincare products'))
