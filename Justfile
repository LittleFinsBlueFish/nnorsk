
manage := "uv run python -m norsk.manage"

@manage *args='':
    {{ manage }} {{ args }}

@runserver *args='':
    {{ manage }} runserver {{ args }}

@runcelery *args='':
    {{ manage }} runcelery {{ args }}

@startapp app_name:
    {{ manage }} startapp {{ app_name }} --template=docs/template
    rm {{ app_name }}/templates/{{ app_name }}/.gitkeep
    mv {{ app_name }} norsk/apps/{{ app_name }}

