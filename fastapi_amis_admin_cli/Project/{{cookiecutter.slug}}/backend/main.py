from starlette.responses import RedirectResponse
from fastapi import FastAPI

from core.adminsite import site
from core.settings import settings

app = FastAPI(debug=settings.debug)

# 安装应用
from apps import {{ cookiecutter.app_slug }}
{{ cookiecutter.app_slug }}.setup(app)

# 挂载后台管理系统
site.mount_app(app)


@app.on_event("startup")
async def startup():
{% if cookiecutter.use_user_auth == "True" %}
    from core.adminsite import auth
    await site.create_db_and_tables()
    await auth.create_role_user(role_key='admin')
    await auth.create_role_user(role_key='vip')
    await auth.create_role_user(role_key='test')
{% endif %}
{% if cookiecutter.use_scheduler == "True" %}
    from core.adminsite import scheduler
    scheduler.start()
{% else %}
    pass
{% endif %}


@app.get('/')
async def index():
    return RedirectResponse(url=site.router_path)


# # 1.配置 CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.allow_origins,  # 允许访问的源
#     allow_credentials=True,  # 支持 cookie
#     allow_methods=["*"],  # 允许使用的请求方法
#     allow_headers=["*"]  # 允许携带的 Headers
# )

# # 2.配置 Swagger UI CDN
# from fastapi.openapi.docs import get_swagger_ui_html
# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         title=f"{app.title} - Swagger UI",
#         oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
#         swagger_js_url="https://unpkg.com/swagger-ui-dist@4/swagger-ui-bundle.js",
#         swagger_css_url="https://unpkg.com/swagger-ui-dist@3/swagger-ui.css",
#     )
