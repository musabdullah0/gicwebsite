from fasthtml.common import *
import httpx
from datetime import datetime

# Initialize FastHTML app
app, rt = fast_app(
    hdrs=(
        Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'),
        Script(src='https://unpkg.com/htmx.org@1.9.10'),
    )
)

# Configuration
MASJID_ID = "xwLVMDKJ"
MAILCHIMP_API_KEY = "your_api_key"
MAILCHIMP_LIST_ID = "your_list_id"
MAILCHIMP_SERVER = "us1"

# Helper function to fetch prayer times
async def get_prayer_times():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://masjidal.com/api/v1/time/range?masjid_id={MASJID_ID}")
            data = response.json()
            
            adhans = data['data']['salah'][0]
            iqamas = data['data']['iqamah'][0]
            
            def clean_time(t):
                return t[:-2] if t else ""
            
            return {
                'fajr': {'adhan': clean_time(adhans.get('fajr')), 'iqama': clean_time(iqamas.get('fajr'))},
                'sunrise': {'adhan': clean_time(adhans.get('sunrise')), 'iqama': None},
                'dhuhr': {'adhan': clean_time(adhans.get('zuhr')), 'iqama': clean_time(iqamas.get('zuhr'))},
                'asr': {'adhan': clean_time(adhans.get('asr')), 'iqama': clean_time(iqamas.get('asr'))},
                'maghrib': {'adhan': clean_time(adhans.get('maghrib')), 'iqama': clean_time(iqamas.get('maghrib'))},
                'isha': {'adhan': clean_time(adhans.get('isha')), 'iqama': clean_time(iqamas.get('isha'))},
            }
    except Exception as e:
        return None

# Components
def navbar():
    return Nav(cls='bg-white shadow-lg sticky top-0 z-50')(
        Div(cls='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8')(
            Div(cls='flex justify-between h-16')(
                Div(cls='flex items-center')(
                    Div(cls='w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-full flex items-center justify-center')(
                        Span('GIC', cls='text-white font-bold text-xl')
                    ),
                    Span('Georgetown Islamic Center', cls='ml-3 text-xl font-bold text-gray-800')
                ),
                Div(cls='hidden md:flex items-center space-x-8')(
                    A('Home', href='/', cls='text-gray-700 hover:text-blue-600 font-medium'),
                    A('About', href='/about', cls='text-gray-700 hover:text-blue-600 font-medium'),
                    A('Education', href='/education', cls='text-gray-700 hover:text-blue-600 font-medium'),
                    A('Donate', href='/donate', cls='bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 font-medium')
                ),
                Button(id='mobile-menu-btn', cls='md:hidden text-gray-700', onclick='document.getElementById("mobile-menu").classList.toggle("hidden")')(
                    '☰'
                )
            )
        ),
        Div(id='mobile-menu', cls='hidden md:hidden bg-white border-t px-2 pt-2 pb-3 space-y-1')(
            A('Home', href='/', cls='block px-3 py-2 text-gray-700 hover:bg-blue-50 rounded-md'),
            A('About', href='/about', cls='block px-3 py-2 text-gray-700 hover:bg-blue-50 rounded-md'),
            A('Education', href='/education', cls='block px-3 py-2 text-gray-700 hover:bg-blue-50 rounded-md'),
            A('Donate', href='/donate', cls='block px-3 py-2 bg-blue-600 text-white rounded-md text-center')
        )
    )

def hero_section():
    return Section(cls='bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20')(
        Div(cls='max-w-7xl mx-auto px-4 text-center')(
            H1('Welcome to Georgetown Islamic Center', cls='text-5xl font-bold mb-4'),
            P('Building a stronger Muslim community through faith, education, and service', cls='text-xl text-blue-100')
        )
    )

def prayer_times_table(times):
    if not times:
        return Div(cls='text-center py-8')(
            P('Unable to load prayer times', cls='text-gray-600')
        )
    
    rows = []
    for name, time in [
        ('Fajr', times['fajr']),
        ('Sunrise', times['sunrise']),
        ('Dhuhr', times['dhuhr']),
        ('Asr', times['asr']),
        ('Maghrib', times['maghrib']),
        ('Isha', times['isha'])
    ]:
        rows.append(
            Tr(cls='border-b border-gray-200 hover:bg-blue-50')(
                Td(name, cls='py-3 px-4 font-semibold text-gray-700'),
                Td(time['adhan'], cls='py-3 px-4 text-center text-gray-600'),
                Td(time['iqama'] if time['iqama'] else '-', cls='py-3 px-4 text-center text-gray-600')
            )
        )
    
    return Div(cls='overflow-x-auto')(
        Table(cls='w-full')(
            Thead(
                Tr(cls='bg-blue-600 text-white')(
                    Th('Prayer', cls='py-3 px-4 text-left rounded-tl-lg'),
                    Th('Adhan', cls='py-3 px-4 text-center'),
                    Th('Iqama', cls='py-3 px-4 text-center rounded-tr-lg')
                )
            ),
            Tbody(cls='bg-white')(*rows)
        )
    )

def vision_section():
    return Section(cls='py-16 bg-white')(
        Div(cls='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8')(
            Div(cls='grid grid-cols-1 lg:grid-cols-2 gap-12')(
                # Vision Content
                Div(
                    H2('GIC Vision', cls='text-3xl font-bold text-gray-800 mb-6'),
                    Div(cls='mb-6 relative pb-[56.25%] h-0 rounded-lg overflow-hidden shadow-lg')(
                        Iframe(src='https://www.youtube.com/embed/YOUR_VIDEO_ID', 
                               cls='absolute top-0 left-0 w-full h-full',
                               allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture',
                               allowfullscreen=True)
                    ),
                    P(Strong('Alhamdulillah! '), 
                      'With the Help and Mercy of Allah ﷻ, and through your generous support, we have successfully closed on the purchase of the 2 acres adjacent to GIC.',
                      cls='text-lg text-gray-700 mb-4'),
                    P('May Allah accept every contribution, place barakah in your wealth, health, and families. May Allah make this property a source of Goodness, unity, and service for generations to come.',
                      cls='text-gray-700 mb-4'),
                    A('Support GIC Expansion', href='/donate', cls='inline-block bg-amber-700 text-white px-8 py-3 rounded-lg hover:bg-amber-800 font-medium text-lg')
                ),
                # Prayer Times
                Div(
                    H2('Prayer Times', cls='text-3xl font-bold text-gray-800 mb-6'),
                    Div(id='prayer-times-container', 
                        hx_get='/api/prayer-times',
                        hx_trigger='load',
                        hx_swap='innerHTML',
                        cls='bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg shadow-lg p-6')(
                        Div(cls='text-center py-8')(
                            P('Loading prayer times...', cls='text-gray-600')
                        )
                    ),
                    # Friday Prayers
                    Div(cls='mt-6 bg-gradient-to-br from-green-50 to-green-100 rounded-lg shadow-lg p-6')(
                        H3('Friday Prayers', cls='text-2xl font-bold text-gray-800 mb-4'),
                        Div(cls='space-y-3')(
                            Div(cls='flex justify-between items-center bg-white rounded-lg p-4 shadow')(
                                Span('First Jummah', cls='font-semibold text-gray-700'),
                                Div(cls='text-right')(
                                    Div('Adhan: 1:00 | Iqama: 1:30', cls='text-sm text-gray-600')
                                )
                            ),
                            Div(cls='flex justify-between items-center bg-white rounded-lg p-4 shadow')(
                                Span('Second Jummah', cls='font-semibold text-gray-700'),
                                Div(cls='text-right')(
                                    Div('Adhan: 2:00 | Iqama: 2:30', cls='text-sm text-gray-600')
                                )
                            )
                        )
                    )
                )
            )
        )
    )

def newsletter_section():
    return Section(cls='py-16 bg-gradient-to-r from-blue-600 to-blue-800')(
        Div(cls='max-w-4xl mx-auto px-4 text-center')(
            H2('Stay Connected', cls='text-3xl font-bold text-white mb-4'),
            P('Subscribe to our newsletter for updates on events, programs, and community news', 
              cls='text-blue-100 mb-8 text-lg'),
            Form(hx_post='/api/subscribe', 
                 hx_target='#newsletter-response',
                 hx_swap='innerHTML',
                 cls='max-w-md mx-auto')(
                Div(cls='flex flex-col sm:flex-row gap-3')(
                    Input(type='email', name='email', placeholder='Enter your email', required=True,
                          cls='flex-1 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300'),
                    Button('Subscribe', type='submit',
                           cls='bg-white text-blue-600 px-8 py-3 rounded-lg hover:bg-gray-100 font-medium')
                )
            ),
            Div(id='newsletter-response', cls='mt-4')
        )
    )

def contact_section():
    return Section(cls='py-16 bg-gray-100')(
        Div(cls='max-w-4xl mx-auto px-4')(
            H2('Get in Touch', cls='text-3xl font-bold text-gray-800 mb-8 text-center'),
            Form(hx_post='/api/contact',
                 hx_target='#contact-response',
                 hx_swap='innerHTML',
                 cls='bg-white rounded-lg shadow-lg p-8')(
                Div(cls='grid grid-cols-1 md:grid-cols-2 gap-6 mb-6')(
                    Div(
                        Label('Name', cls='block text-gray-700 font-medium mb-2'),
                        Input(type='text', name='name', required=True,
                              cls='w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500')
                    ),
                    Div(
                        Label('Email', cls='block text-gray-700 font-medium mb-2'),
                        Input(type='email', name='email', required=True,
                              cls='w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500')
                    )
                ),
                Div(cls='mb-6')(
                    Label('Message', cls='block text-gray-700 font-medium mb-2'),
                    Textarea(name='message', rows='5', required=True,
                             cls='w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500')
                ),
                Button('Send Message', type='submit',
                       cls='w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 font-medium text-lg')
            ),
            Div(id='contact-response', cls='mt-4')
        )
    )

def footer():
    return Footer(cls='bg-gray-800 text-white py-12')(
        Div(cls='max-w-7xl mx-auto px-4')(
            Div(cls='grid grid-cols-1 md:grid-cols-3 gap-8')(
                Div(
                    H3('Georgetown Islamic Center', cls='text-xl font-bold mb-4'),
                    P('Serving the Muslim community in Georgetown and surrounding areas', cls='text-gray-300')
                ),
                Div(
                    H3('Contact', cls='text-xl font-bold mb-4'),
                    Div(cls='space-y-2 text-gray-300')(
                        P('📍 Round Rock, TX 78665'),
                        P('📞 (512) 522-4595'),
                        P('✉️ admin@gicmasjid.org')
                    )
                ),
                Div(
                    H3('Quick Links', cls='text-xl font-bold mb-4'),
                    Div(cls='space-y-2')(
                        A('About Us', href='/about', cls='block text-gray-300 hover:text-white'),
                        A('Education', href='/education', cls='block text-gray-300 hover:text-white'),
                        A('Donate', href='/donate', cls='block text-gray-300 hover:text-white')
                    )
                )
            ),
            Div(cls='border-t border-gray-700 mt-8 pt-8 text-center text-gray-400')(
                P('© 2025 Georgetown Islamic Center. All rights reserved.')
            )
        )
    )

# Routes
@rt('/')
def get():
    return Title('Georgetown Islamic Center'), Main(
        navbar(),
        hero_section(),
        vision_section(),
        newsletter_section(),
        contact_section(),
        footer()
    )

@rt('/api/prayer-times')
async def get():
    times = await get_prayer_times()
    return prayer_times_table(times)

@rt('/api/subscribe')
async def post(email: str):
    try:
        if not MAILCHIMP_API_KEY or MAILCHIMP_API_KEY == "your_api_key":
            return Div(cls='bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded')(
                'Mailchimp not configured. Please set MAILCHIMP_API_KEY.'
            )
        
        url = f"https://{MAILCHIMP_SERVER}.api.mailchimp.com/3.0/lists/{MAILCHIMP_LIST_ID}/members"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                auth=("anystring", MAILCHIMP_API_KEY),
                json={"email_address": email, "status": "subscribed"}
            )
            
            if response.status_code in [200, 201]:
                return Div(cls='bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded')(
                    'Successfully subscribed to our newsletter!'
                )
            else:
                raise Exception("Subscription failed")
    except Exception as e:
        return Div(cls='bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded')(
            'Failed to subscribe. Please try again.'
        )

@rt('/api/contact')
async def post(name: str, email: str, message: str):
    # Log contact form (in production, send email or save to database)
    print(f"Contact: {name} ({email}): {message}")
    
    return Div(cls='bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded')(
        'Thank you for your message! We\'ll get back to you soon.'
    )

@rt('/about')
def get():
    return Title('About Us'), Main(
        navbar(),
        Section(cls='py-16')(
            Div(cls='max-w-4xl mx-auto px-4')(
                H1('About Us', cls='text-4xl font-bold mb-8'),
                P('Coming soon...', cls='text-xl text-gray-700')
            )
        ),
        footer()
    )

@rt('/education')
def get():
    return Title('Education'), Main(
        navbar(),
        Section(cls='py-16')(
            Div(cls='max-w-4xl mx-auto px-4')(
                H1('Education Programs', cls='text-4xl font-bold mb-8'),
                P('Coming soon...', cls='text-xl text-gray-700')
            )
        ),
        footer()
    )

@rt('/donate')
def get():
    return Title('Donate'), Main(
        navbar(),
        Section(cls='py-16')(
            Div(cls='max-w-4xl mx-auto px-4')(
                H1('Support GIC', cls='text-4xl font-bold mb-8'),
                P('Coming soon...', cls='text-xl text-gray-700')
            )
        ),
        footer()
    )

serve()