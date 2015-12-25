# Require any additional compass plugins here.
# require 'sassy-buttons'

# Set this to the root of your project when deployed:
http_path = "/static/assets/"
css_dir = "../assets/css"
sass_dir = "sass"
images_dir = "images"
generated_images_dir = "../assets/images/"
javascripts_dir = "javascripts"

#enable sourcemaps on production only
# sourcemap = (environment == :production) ? false : true
sourcemap = true

add_import_path "../vendor/bootstrap-sass-official/assets/stylesheets"

http_images_path = "/static/assets/images/"

# You can select your preferred output style here (can be overridden via the command line):
output_style = :expanded

# To enable relative paths to assets via compass helper functions. Uncomment:
# relative_assets = true

# To disable debugging comments that display the original location of your selectors. Uncomment:
# line_comments = false

preferred_syntax = :scss
encoding = "utf-8"
Encoding.default_external = 'utf-8'
