from setuptools import setup

setup(
    name='fruity_display_menu',
    version='1.0.0',    
    description='Simple menu library for CircuitPython devices, designed for Adafruit RP2040 macropad.',
    url='https://git.therode.net/jrode/fruity_menu',
    author='Jay Rode',
    author_email='jay@rode.dev',
    license='Mozilla Public License 2.0',
    packages=['fruity_menu'],
    install_requires=['adafruit_blinka_displayio',
                      'adafruit_circuitpython_display_text',
                      'adafruit_circuitpython_displayio_sh1106',
                      ],

    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)
