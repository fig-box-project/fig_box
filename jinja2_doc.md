# 神社2语法

## 获取文章数据

> 直接使用类似 `{{ pagedata.title }}` 的来进行获取文章数据<br>
获取id时就 `{{ page_data.id }}`<br>

<br>

# 以下摘自[jinja2文档](http://docs.jinkan.org/docs/jinja2/templates.html)

## 获取属性

> 以下两种方法功能相同

```
{{ article.title }}
{{ article['title'] }}
```

## [for语法示例](http://docs.jinkan.org/docs/jinja2/templates.html#for)

> 普通

```
{% for user in users %}
    <li><a href="{{ user.url }}">{{ user.username }}</a></li>
{% endfor %}
```

> 想去除中间空白时:

```
{% for item in seq -%}
    {{ item }}
{%- endfor %}
```

> 想在数组无成员时显示些什么可以加else

```
{% for user in users %}
    <li>{{ user.username|e }}</li>
{% else %}
    <li><em>no users found</em></li>
{% endfor %}
```

## [if语法(与for差不多)(减号可以加在前面以去除前面的空格)](http://docs.jinkan.org/docs/jinja2/templates.html#if)  _|_ [额外链接](http://docs.jinkan.org/docs/jinja2/templates.html#if-expression)

```
{%- if foo -%}
    <li><a href="{{ user.url }}">{{ user.username }}</a></li>
{%- endif %}
```

## 不转义

> 想输出{{时

```
{{ '{{' }}
```

> raw区块中将原样输出

```
{% raw %}
    <ul>
    {% for item in seq %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
{% endraw %}
```

## 过滤器(其实相当于后端函数调用)

```
<!-- 带参数的 -->
{{ 变量 | 函数名(*args)}}

<!-- 不带参数可以省略括号 -->
{{ 变量 | 函数名 }}

<!-- 文本块调用（将中间的所有文字都作为变量内容传入到过滤器中） -->
{% filter upper %}
    一大堆文字
{% endfilter %}
```

# 自带过滤器

```
safe：禁用转义
<p>{{ '<em>hello</em>' | safe }}</p>

capitalize：把变量值的首字母转成大写，其余字母转小写
<p>{{ 'hello' | capitalize }}</p>

lower：把值转成小写
<p>{{ 'HELLO' | lower }}</p>

upper：把值转成大写
<p>{{ 'hello' | upper }}</p>

title：把值中的每个单词的首字母都转成大写
<p>{{ 'hello' | title }}</p>

reverse：字符串反转
<p>{{ 'olleh' | reverse }}</p>

format：格式化输出
<p>{{ '%s is %d' | format('name',17) }}</p>

striptags：渲染之前把值中所有的 HTML 标签都删掉
<p>{{ '<em>hello</em>' | striptags }}</p>

truncate: 字符串截断
<p>{{ 'hello every one' | truncate(9)}}</p>
```