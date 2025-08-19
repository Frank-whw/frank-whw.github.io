def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    """
    
    @env.macro
    def BEGIN_TOC():
        """开始TOC标记"""
        return '<div class="toc-container">'
    
    @env.macro
    def END_TOC():
        """结束TOC标记"""
        return '</div>'
    
    # 处理TOC内容的宏
    @env.macro
    def toc_section(title, items):
        """生成TOC部分"""
        html = f'<h3>{title}</h3><ul>'
        for item in items:
            if isinstance(item, dict):
                for key, value in item.items():
                    html += f'<li><a href="../{value}/">{key}</a></li>'
            else:
                html += f'<li>{item}</li>'
        html += '</ul>'
        return html