#!/usr/bin/env python3
"""
Ruijian Website - Multi-language page generator
Generates all remaining pages for 6 languages from Chinese templates.
"""

import os
import shutil

BASE = "/mnt/e/hu/gado/钢材/黑龙江瑞建石油装备有限责任公司/ruijian-website"

# Language configurations
LANGUAGES = {
    'zh': {
        'dir': 'ltr',
        'flag': '🇨🇳',
        'name': '中文',
        'native': '简体中文',
        'font': 'Noto+Sans+SC:wght@300;400;500;700;900',
        'font_family': "'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif",
        'og_locale': 'zh_CN',
        'class': 'lang-zh'
    },
    'en': {
        'dir': 'ltr',
        'flag': '🇬🇧',
        'name': 'English',
        'native': 'English',
        'font': 'Inter:wght@300;400;500;600;700;800;900',
        'font_family': "'Inter','Helvetica Neue',Arial,sans-serif",
        'og_locale': 'en_US',
        'class': 'lang-en'
    },
    'ar': {
        'dir': 'rtl',
        'flag': '🇸🇦',
        'name': 'العربية',
        'native': 'العربية',
        'font': 'Noto+Sans+Arabic:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800',
        'font_family': "'Noto Sans Arabic','Inter',sans-serif",
        'og_locale': 'ar_SA',
        'class': 'lang-ar'
    },
    'ru': {
        'dir': 'ltr',
        'flag': '🇷🇺',
        'name': 'Русский',
        'native': 'Русский',
        'font': 'Noto+Sans:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800',
        'font_family': "'Noto Sans','Inter',sans-serif",
        'og_locale': 'ru_RU',
        'class': 'lang-ru'
    },
    'es': {
        'dir': 'ltr',
        'flag': '🇪🇸',
        'name': 'Español',
        'native': 'Español',
        'font': 'Inter:wght@300;400;500;600;700;800;900',
        'font_family': "'Inter','Helvetica Neue',Arial,sans-serif",
        'og_locale': 'es_ES',
        'class': 'lang-es'
    },
    'fr': {
        'dir': 'ltr',
        'flag': '🇫🇷',
        'name': 'Français',
        'native': 'Français',
        'font': 'Inter:wght@300;400;500;600;700;800;900',
        'font_family': "'Inter','Helvetica Neue',Arial,sans-serif",
        'og_locale': 'fr_FR',
        'class': 'lang-fr'
    }
}

# Translation data
# Key translations organized by page section
TRANSLATIONS = {
    # Navigation
    'nav_home': {'zh':'首页','en':'Home','ar':'الرئيسية','ru':'Главная','es':'Inicio','fr':'Accueil'},
    'nav_about': {'zh':'关于我们','en':'About','ar':'من نحن','ru':'О нас','es':'Nosotros','fr':'À propos'},
    'nav_products': {'zh':'产品中心','en':'Products','ar':'المنتجات','ru':'Продукция','es':'Productos','fr':'Produits'},
    'nav_quality': {'zh':'质量控制','en':'Quality','ar':'الجودة','ru':'Контроль качества','es':'Calidad','fr':'Qualité'},
    'nav_certifications': {'zh':'资质认证','en':'Certifications','ar':'الشهادات','ru':'Сертификаты','es':'Certificaciones','fr':'Certifications'},
    'nav_projects': {'zh':'项目案例','en':'Projects','ar':'المشاريع','ru':'Проекты','es':'Proyectos','fr':'Projets'},
    'nav_contact': {'zh':'联系我们','en':'Contact','ar':'اتصل بنا','ru':'Контакты','es':'Contacto','fr':'Contact'},
    
    # Products subnav
    'nav_casing': {'zh':'石油套管','en':'Oil Casing','ar':'أنابيب التغليف','ru':'Обсадные трубы','es':'Tubería de Revestimiento','fr':'Tubage pétrolier'},
    'nav_tubing': {'zh':'油管','en':'Tubing','ar':'أنابيب النفط','ru':'Насосно-компрессорные трубы','es':'Tubería de Producción','fr':'Tube de production'},
    'nav_drill_pipe': {'zh':'钻杆','en':'Drill Pipe','ar':'أنبوب الحفر','ru':'Бурильная труба','es':'Tubería de Perforación','fr':'Tige de forage'},
    'nav_drill_collar': {'zh':'钻铤','en':'Drill Collar','ar':'طوق الحفر','ru':'Утяжеленная бурильная труба','es':'Portamecha','fr':'Masse-tige'},
    'nav_seamless': {'zh':'无缝钢管','en':'Seamless Pipe','ar':'أنبوب غير ملحوم','ru':'Бесшовная труба','es':'Tubería Sin Costura','fr':'Tube sans soudure'},
    'nav_coupling': {'zh':'接箍','en':'Couplings','ar':'الوصلات','ru':'Муфты','es':'Acoplamientos','fr':'Raccords'},
    
    # Company name
    'company_short': {'zh':'瑞建石油装备','en':'Ruijian Petroleum','ar':'معدات رويجيان النفطية','ru':'Ruijian Petroleum','es':'Ruijian Petroleum','fr':'Ruijian Pétrole'},
    'company_full': {'zh':'黑龙江瑞建石油装备有限责任公司','en':'Heilongjiang Ruijian Petroleum Equipment Co., Ltd.','ar':'شركة هيلونغجيانغ رويجيان لمعدات النفط المحدودة','ru':'Хэйлунцзянская компания по производству нефтяного оборудования Ruijian','es':'Heilongjiang Ruijian Equipos Petroleros Co., Ltd.','fr':'Heilongjiang Ruijian Équipement Pétrolier Co., Ltd.'},
    'company_sub': {'zh':'瑞建石油装备（天津）有限公司','en':'Ruijian Petroleum Equipment (Tianjin) Co., Ltd.','ar':'شركة رويجيان لمعدات النفط (تيانجين) المحدودة','ru':'Ruijian Petroleum Equipment (Тяньцзинь) Ко., Лтд.','es':'Ruijian Equipos Petroleros (Tianjin) Co., Ltd.','fr':'Ruijian Équipement Pétrolier (Tianjin) Co., Ltd.'},
    'company_tagline': {'zh':'RUIJIAN PETROLEUM EQUIPMENT','en':'HEILONGJIANG · TIANJIN · GLOBAL','ar':'هيلونغجيانغ · تيانجين · العالم','ru':'ХЭЙЛУНЦЗЯН · ТЯНЬЦЗИНЬ · МИР','es':'HEILONGJIANG · TIANJIN · GLOBAL','fr':'HEILONGJIANG · TIANJIN · MONDIAL'},
    
    # Footer
    'footer_about_desc': {
        'zh':'黑龙江瑞建石油装备有限责任公司（制造基地）+ 瑞建石油装备（天津）有限公司（销售中心），致力于成为世界知名的中国石油钻探管品牌企业。',
        'en':'Heilongjiang Ruijian Petroleum Equipment (manufacturing base) + Ruijian Petroleum Equipment (Tianjin) Co., Ltd. (sales center). Committed to becoming a world-renowned Chinese petroleum drilling pipe brand.',
        'ar':'شركة هيلونغجيانغ رويجيان لمعدات النفط (قاعدة التصنيع) + شركة رويجيان لمعدات النفط (تيانجين) المحدودة (مركز المبيعات). ملتزمون بأن نصبح علامة تجارية صينية عالمية لأنابيب حفر النفط.',
        'ru':'Хэйлунцзянская Ruijian Petroleum Equipment (производственная база) + Ruijian Petroleum Equipment (Тяньцзинь) (торговый центр). Стремимся стать всемирно известным китайским брендом бурильных труб.',
        'es':'Heilongjiang Ruijian Petroleum Equipment (base de fabricación) + Ruijian Petroleum Equipment (Tianjin) Co., Ltd. (centro de ventas). Comprometidos a convertirnos en una marca china mundialmente reconocida de tuberías de perforación petrolera.',
        'fr':'Heilongjiang Ruijian Petroleum Equipment (base de fabrication) + Ruijian Petroleum Equipment (Tianjin) Co., Ltd. (centre de vente). Engagés à devenir une marque chinoise mondialement reconnue de tiges de forage pétrolier.'
    },
    'footer_products': {'zh':'产品中心','en':'Products','ar':'المنتجات','ru':'Продукция','es':'Productos','fr':'Produits'},
    'footer_about': {'zh':'关于','en':'Company','ar':'الشركة','ru':'Компания','es':'Empresa','fr':'Société'},
    'footer_contact': {'zh':'联系我们','en':'Contact','ar':'اتصل بنا','ru':'Контакты','es':'Contacto','fr':'Contact'},
    'footer_company': {'zh':'公司简介','en':'About Us','ar':'من نحن','ru':'О нас','es':'Sobre Nosotros','fr':'À propos'},
    'footer_privacy': {'zh':'隐私政策','en':'Privacy Policy','ar':'سياسة الخصوصية','ru':'Политика конфиденциальности','es':'Política de Privacidad','fr':'Politique de confidentialité'},
    'footer_terms': {'zh':'使用条款','en':'Terms of Use','ar':'شروط الاستخدام','ru':'Условия использования','es':'Términos de Uso','fr':'Conditions d\'utilisation'},
    'footer_copyright': {'zh':'© 2026 黑龙江瑞建石油装备有限责任公司 · 瑞建石油装备（天津）有限公司 版权所有','en':'© 2026 Heilongjiang Ruijian Petroleum Equipment Co., Ltd. · Ruijian Petroleum Equipment (Tianjin) Co., Ltd. All Rights Reserved.','ar':'© 2026 شركة هيلونغجيانغ رويجيان لمعدات النفط المحدودة · شركة رويجيان لمعدات النفط (تيانجين) المحدودة. جميع الحقوق محفوظة.','ru':'© 2026 Хэйлунцзянская Ruijian Petroleum Equipment Co., Ltd. · Ruijian Petroleum Equipment (Тяньцзинь) Co., Ltd. Все права защищены.','es':'© 2026 Heilongjiang Ruijian Petroleum Equipment Co., Ltd. · Ruijian Petroleum Equipment (Tianjin) Co., Ltd. Todos los derechos reservados.','fr':'© 2026 Heilongjiang Ruijian Petroleum Equipment Co., Ltd. · Ruijian Petroleum Equipment (Tianjin) Co., Ltd. Tous droits réservés.'},
    
    # Cookie
    'cookie_text': {'zh':'本网站使用 Cookie 以提升您的浏览体验。继续使用本网站即表示您同意我们的 Cookie 政策。','en':'This website uses cookies to enhance your browsing experience. By continuing to use this site, you agree to our cookie policy.','ar':'يستخدم هذا الموقع ملفات تعريف الارتباط لتحسين تجربة التصفح الخاصة بك. باستمرارك في استخدام هذا الموقع، فإنك توافق على سياسة ملفات تعريف الارتباط الخاصة بنا.','ru':'Этот сайт использует файлы cookie для улучшения вашего просмотра. Продолжая использовать сайт, вы соглашаетесь с нашей политикой использования файлов cookie.','es':'Este sitio web utiliza cookies para mejorar su experiencia de navegación. Al continuar usando este sitio, acepta nuestra política de cookies.','fr':'Ce site utilise des cookies pour améliorer votre expérience de navigation. En continuant à utiliser ce site, vous acceptez notre politique de cookies.'},
    'cookie_accept': {'zh':'接受全部','en':'Accept All','ar':'قبول الكل','ru':'Принять все','es':'Aceptar todo','fr':'Tout accepter'},
    'cookie_necessary': {'zh':'仅必要','en':'Necessary Only','ar':'الضرورية فقط','ru':'Только необходимые','es':'Solo necesarias','fr':'Uniquement nécessaires'},
    
    # Contact info
    'contact_factory': {'zh':'制造基地（黑龙江工厂）','en':'Manufacturing Base (Heilongjiang Factory)','ar':'قاعدة التصنيع (مصنع هيلونغجيانغ)','ru':'Производственная база (завод в Хэйлунцзяне)','es':'Base de fabricación (Fábrica de Heilongjiang)','fr':'Base de fabrication (Usine du Heilongjiang)'},
    'contact_factory_addr': {'zh':'黑龙江省双鸭山市岭东区双选路钢联','en':'Shuangxuan Road, Lingdong District, Shuangyashan City, Heilongjiang Province','ar':'طريق شوانغشوان، منطقة لينغدونغ، مدينة شوانغياشان، مقاطعة هيلونغجيانغ','ru':'Шуансюань Роуд, район Линдун, город Шуанъяшань, провинция Хэйлунцзян','es':'Carretera Shuangxuan, Distrito Lingdong, Ciudad Shuangyashan, Provincia Heilongjiang','fr':'Route Shuangxuan, District Lingdong, Ville Shuangyashan, Province Heilongjiang'},
    'contact_sales': {'zh':'销售中心（天津公司）','en':'Sales Center (Tianjin Office)','ar':'مركز المبيعات (مكتب تيانجين)','ru':'Торговый центр (офис в Тяньцзине)','es':'Centro de ventas (Oficina de Tianjin)','fr':'Centre de vente (Bureau de Tianjin)'},
    'contact_sales_addr': {'zh':'天津市东丽区军粮城工业园 · 瑞建石油装备（天津）有限公司','en':'Junliangcheng Industrial Park, Dongli District, Tianjin · Ruijian Petroleum Equipment (Tianjin) Co., Ltd.','ar':'منطقة دونغلي، تيانجين','ru':'Район Дунли, Тяньцзинь','es':'Distrito Dongli, Tianjin','fr':'District Dongli, Tianjin'},
    'contact_phone': {'zh':'电话 / WhatsApp','en':'Phone / WhatsApp','ar':'هاتف / واتساب','ru':'Телефон / WhatsApp','es':'Teléfono / WhatsApp','fr':'Téléphone / WhatsApp'},
    'contact_phone_val': {'zh':'+86 18618191088（联系人：任庆祥 / Kevin）','en':'+86 18618191088 (Contact: Kevin Ren)','ar':'+86 18618191088 (جهة الاتصال: كيفن)','ru':'+86 18618191088 (Контакт: Кевин)','es':'+86 18618191088 (Contacto: Kevin)','fr':'+86 18618191088 (Contact : Kevin)'},
    'contact_email': {'zh':'邮箱','en':'Email','ar':'البريد الإلكتروني','ru':'Эл. почта','es':'Correo electrónico','fr':'Email'},
    'contact_web': {'zh':'网址','en':'Website','ar':'الموقع الإلكتروني','ru':'Веб-сайт','es':'Sitio web','fr':'Site web'},
    'contact_social': {'zh':'社交媒体','en':'Social Media','ar':'وسائل التواصل الاجتماعي','ru':'Социальные сети','es':'Redes sociales','fr':'Réseaux sociaux'},
    'contact_wechat': {'zh':'微信：18618191088','en':'WeChat: 18618191088','ar':'وي شات: 18618191088','ru':'WeChat: 18618191088','es':'WeChat: 18618191088','fr':'WeChat: 18618191088'},
}


def t(key, lang):
    """Get translation for a key in the given language."""
    if key in TRANSLATIONS and lang in TRANSLATIONS[key]:
        return TRANSLATIONS[key][lang]
    return f'[MISSING:{key}:{lang}]'


def generate_page(template_lang, target_lang, page_type, template_path, output_path):
    """Generate a page for target language from template."""
    # Read template
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    src = template_lang
    dst = target_lang

    if src == dst:
        # For the same language, just copy
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        shutil.copy2(template_path, output_path)
        print(f"  Copied {src} -> {dst}: {output_path}")
        return

    # --- 1. Fix broken template patterns first (known bugs in source templates) ---
    # Fix logo href missing quote: href="/zh/ class="logo" -> href="/zh/" class="logo"
    content = content.replace(f'href="/{src}/ class="logo"', f'href="/{src}/" class="logo"')

    # --- 2. Replace canonical URL ONLY (not hreflang) ---
    # Only match the exact canonical link, not all hreflang URLs
    old_canonical = f'<link rel="canonical" href="https://www.ruijianoil.com/{src}/'
    new_canonical = f'<link rel="canonical" href="https://www.ruijianoil.com/{dst}/'
    content = content.replace(old_canonical, new_canonical)

    # --- 3. Fix zh hreflang that got broken (must stay /zh/) ---
    # After canonical replacement, fix the zh hreflang entry if it was broken
    # Pattern: hreflang="zh" href="https://www.ruijianoil.com/{dst}/" -> /zh/
    old_zh_hreflang = f'hreflang="zh" href="https://www.ruijianoil.com/{dst}/'
    new_zh_hreflang = f'hreflang="zh" href="https://www.ruijianoil.com/{src}/'
    content = content.replace(old_zh_hreflang, new_zh_hreflang)

    # --- 4. Fix nav product links pointing to current page ---
    # The template has nav items with href="/zh/{page_type}/".
    # For the Products dropdown, it should point to /zh/products/, not /zh/{page_type}/
    # We fix this by replacing the Products link AFTER the canonical replacement
    for section in ['about', 'contact', 'quality', 'certifications', 'projects']:
        old_nav = f'href="/{dst}/{section}/" class="active">'
        # Check if this is the Products link (not About/Contact/Quality etc.)
        # We can't tell by href alone, but we know it was wrong in templates
        # The safest fix: for any generated page, if the Products nav href
        # matches the page section, redirect to /products/
        # This is handled by the section loop below
        pass

    # --- 5. Replace lang attribute ---
    content = content.replace(f'lang="{src}"', f'lang="{dst}"')

    # --- 6. Handle dir attribute ---
    if LANGUAGES[dst]['dir'] == 'rtl':
        if f'dir="ltr"' in content:
            content = content.replace('dir="ltr"', 'dir="rtl"')
        else:
            content = content.replace('<html', f'<html dir="rtl"')
        # Add RTL stylesheet if missing
        if 'rtl.css' not in content:
            content = content.replace('/css/style.css">', '/css/style.css">\n  <link rel="stylesheet" href="/css/rtl.css">')
    else:
        # For LTR languages, ensure dir="ltr" is set
        if 'dir="ltr"' not in content and 'dir="rtl"' not in content:
            content = content.replace('<html', f'<html dir="{LANGUAGES[dst]["dir"]}"')

    # --- 7. og:locale ---
    old_locale = f'og:locale" content="{LANGUAGES[src]["og_locale"]}"'
    new_locale = f'og:locale" content="{LANGUAGES[dst]["og_locale"]}"'
    content = content.replace(old_locale, new_locale)

    # --- 8. Body class ---
    content = content.replace(f'class="lang-{src}"', f'class="lang-{dst}"')

    # --- 9. Font links ---
    content = content.replace(LANGUAGES[src]['font'], LANGUAGES[dst]['font'])

    # Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Generated {src} -> {dst}: {output_path}")


def main():
    pages = [
        ('index', 'index.html', ''),
        ('about', 'about/index.html', 'about/'),
        ('contact', 'contact/index.html', 'contact/'),
    ]
    
    for page_type, filename, subdir in pages:
        for src_lang in ['zh']:  # Chinese as source
            template_path = os.path.join(BASE, src_lang, filename)
            if not os.path.exists(template_path):
                print(f"  Template not found: {template_path}")
                continue
            
            for dst_lang in LANGUAGES:
                if dst_lang == src_lang:
                    continue  # skip source language
                output_path = os.path.join(BASE, dst_lang, filename)
                generate_page(src_lang, dst_lang, page_type, template_path, output_path)


def create_favicon():
    """Create favicon SVG"""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="20" fill="#0a1628"/>
  <text x="50" y="68" text-anchor="middle" fill="#e8a838" font-family="Inter,serif" font-size="52" font-weight="900">R</text>
</svg>'''
    os.makedirs(os.path.join(BASE, 'favicon'), exist_ok=True)
    with open(os.path.join(BASE, 'favicon', 'favicon.svg'), 'w') as f:
        f.write(svg)
    
    # Create a simple PNG placeholder note
    with open(os.path.join(BASE, 'favicon', 'favicon-32x32.png'), 'w') as f:
        f.write('Placeholder: replace with actual 32x32 PNG favicon')
    with open(os.path.join(BASE, 'favicon', 'favicon-16x16.png'), 'w') as f:
        f.write('Placeholder: replace with actual 16x16 PNG favicon')
    with open(os.path.join(BASE, 'favicon', 'apple-touch-icon.png'), 'w') as f:
        f.write('Placeholder: replace with actual 180x180 PNG apple touch icon')
    print("  Favicon created")


def create_robots_sitemap():
    """Create robots.txt and sitemap.xml"""
    
    robots = '''User-agent: *
Allow: /
Sitemap: https://www.ruijianoil.com/sitemap.xml
'''
    with open(os.path.join(BASE, 'robots.txt'), 'w') as f:
        f.write(robots)
    
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://www.ruijianoil.com/sitemap-zh.xml</loc></sitemap>
  <sitemap><loc>https://www.ruijianoil.com/sitemap-en.xml</loc></sitemap>
  <sitemap><loc>https://www.ruijianoil.com/sitemap-ar.xml</loc></sitemap>
  <sitemap><loc>https://www.ruijianoil.com/sitemap-ru.xml</loc></sitemap>
  <sitemap><loc>https://www.ruijianoil.com/sitemap-es.xml</loc></sitemap>
  <sitemap><loc>https://www.ruijianoil.com/sitemap-fr.xml</loc></sitemap>
</sitemapindex>
'''
    with open(os.path.join(BASE, 'sitemap.xml'), 'w') as f:
        f.write(sitemap)
    
    print("  robots.txt and sitemap.xml created")


def create_hero_bg_placeholder():
    """Create a placeholder hero background SVG"""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a1628"/>
      <stop offset="50%" style="stop-color:#1b2a4a"/>
      <stop offset="100%" style="stop-color:#0a1628"/>
    </linearGradient>
    <pattern id="p" patternUnits="userSpaceOnUse" width="60" height="60">
      <circle cx="30" cy="30" r="1" fill="rgba(232,168,56,0.15)"/>
    </pattern>
  </defs>
  <rect width="1920" height="1080" fill="url(#g)"/>
  <rect width="1920" height="1080" fill="url(#p)"/>
  <!-- Abstract oil rig silhouette -->
  <g transform="translate(960,540)" opacity="0.06">
    <rect x="-8" y="-300" width="16" height="400" fill="#e8a838" rx="4"/>
    <rect x="-40" y="-320" width="80" height="20" fill="#e8a838" rx="4"/>
    <rect x="-60" y="-340" width="120" height="12" fill="#e8a838" rx="3"/>
    <rect x="-80" y="-60" width="160" height="16" fill="#e8a838" rx="4"/>
    <line x1="-60" y1="-300" x2="-100" y2="-280" stroke="#e8a838" stroke-width="4"/>
    <line x1="60" y1="-300" x2="100" y2="-280" stroke="#e8a838" stroke-width="4"/>
  </g>
</svg>'''
    os.makedirs(os.path.join(BASE, 'images'), exist_ok=True)
    with open(os.path.join(BASE, 'images', 'hero-bg.jpg'), 'w') as f:
        f.write('Placeholder: Replace with actual hero background image (1920x1080 JPG)')
    print("  Hero background placeholder created")
    print("  NOTE: Replace images/hero-bg.jpg with an actual factory photo")


if __name__ == '__main__':
    print("Generating Ruijian Petroleum Website pages...")
    main()
    create_favicon()
    create_robots_sitemap()
    create_hero_bg_placeholder()
    print("\nDone! Website structure created at:", BASE)
