JAZZMIN_SETTINGS: dict = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Transitgroup.uz",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Transitgroup.uz",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "assets/img/site_icon.svg",
    "login_logo": "assets/img/site_icon.svg",
    "login_logo_dark": "assets/img/site_icon.svg",
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "assets/img/site_icon.svg",
    # Welcome text on the login screen
    "welcome_sign": "Добро пожаловать на Transitgroup.uz!",
    # Copyright on the footer
    "copyright": "Transitgroup.uz",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "",
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {
            "name": "Home",
            "url": "admin:index",
            "permissions": ["auth.view_user"],
        },
        # external url that opens in a new window (Permissions can be added)
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [{"model": "users.user"}],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": False,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        # "common.Region",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "common": "fas fa-cubes",
        "driver": "fas fa-taxi",
        "order": "fas fa-road",
        "users": "fas fa-users",
        "users.User": "fas fa-user",
        "common.Promocode": "fas fa-file-alt",
        "common.UserPromocode": "fas fa-share-alt",
        "driver.Driver": "fas fa-taxi",
        "order.Location": "fas fa-map",
        "order.Order": "fas fa-tasks",
        "order.Trip": "fas fa-route",
        "order.Request": "fas fa-clock",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-folder",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "assets/css/main.css",
    "custom_js": "assets/js/admin.js",
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,
    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-lightblue",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-lightblue",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "litera",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": False,
}
