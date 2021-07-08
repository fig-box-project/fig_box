import html2text
from starlette.requests import Request

from fastapi import APIRouter, HTTPException, Depends

from app.models.auth.auth import AuthFilter
from app.models.log.log_tools import LogTools
from app.models.tools import Tools


def test_route(bp: APIRouter, test_auth):
    # @bp.get('/packup/directory', description='打包文件夹')
    # async def packup():
    #     connector = InputZipDirConnector(
    #         "packup", "test.zip", ["settings.yml", "files/templates"], False)
    #     # connector.set_zip_mode(InputZipDirConnector.WRAP_IN_ROOT)
    #     # connector.set_zip_mode(InputZipDirConnector.WRAP_WITH_INDEX)
    #     connector.set_zip_mode(InputZipDirConnector.WRAP_WITH_PATH)
    #     await connector.packup()
    #
    #     # connector = OutputUnzipConnector('packup/test.zip')
    #     # connector.output()
    #
    # @bp.get('/packup/download', description="Download")
    # async def download():
    #     from app.models.assets.input_assets_connector.InputDownloadConnector import InputDownloadConnector
    #     connector = InputDownloadConnector(
    #         "test", "tt312.jpg",
    #         "https://lh3.googleusercontent.com/ogw/ADGmqu8m5HjUhjl1CgV_0NyPrbBTAcsgpWMC2p1LSi0=s64-c-mo")
    #     await connector.packup()
    #
    # @bp.get('/unzip/{l}')
    # def unzip(l: int):
    #     return 5 / 0
    #     # secrets.compare_digest()
    #
    # @bp.get('/test')
    # def test():
    #     print(type(PageMdl))
    #     print(type(DeclarativeMeta))
    #     print(isinstance(PageMdl, DeclarativeMeta))
    #     print(PageMdl.__mro__)
    #     print(PageMdl in PageMdl.__mro__)
    #
    # @bp.get('/category')
    # def category(id: int, db: Session = Depends(database.get_db)):
    #     c: mdl.Category = db.query(mdl.Category).filter_by(id=id).first()
    #
    #     return c.father
    #
    @bp.get('/rere')
    def rere(request: Request):
        return request.headers

    #
    # @bp.get('/settings')
    # def setting():
    #     settings.value['a'] = 'b'
    #
    @bp.get('/log')
    def log():
        LogTools.test()

    @bp.get('/logint')
    def login(user=Depends(AuthFilter(test_auth).ca)):
        print(user.id)

    @bp.get('/test')
    def test():
        htm = '<div class="index-module_articleWrap_2Zphx"><div class="index-module_mediaWrap_213jB"><!--14--><!--15--><div class="index-module_contentImg_JmmC0"><img src="http://pics2.baidu.com/feed/63d0f703918fa0ec97b8081fcfa617e83d6ddb59.jpeg?token=6f508db88efe723ceaabb6d6ee121584&amp;s=DE0327C346230F052999F0300300F050" width="640" class="index-module_large_1mscr"><!--18--></div><!--16--><!--19--><!--20--><!--21--></div><div class="index-module_textWrap_3ygOc"><p><span class="bjh-p">如何在PC上继续进行Witcher 3 Switch的进度，反之亦然？在PC上玩《巫师3》是最好的玩法-当然，<span class="bjh-strong">我们</span>会这样说-出门在外时还可以有其他选择。现在，您可以花很多时间在Skellige上奔腾奔波，然后在诺维格勒（Novigrad）到Nintendo Switch徘徊，并在旅途中增加数百个小时。<span class="bjh-br"></span></span></p><!--22--><!--23--><!--24--><!--25--><!--26--><!--27--></div><div class="index-module_textWrap_3ygOc"><p><span class="bjh-p">那么，如何转移您的Witcher 3 Switch端口保存？值得庆幸的是，它既简单又好用，根本不需要时间。让我们开始吧。</span></p><!--28--><!--29--><!--30--><!--31--><!--32--><!--33--></div><div class="index-module_textWrap_3ygOc"><p><span class="bjh-h3">第一步：启用云保存</span></p><!--34--><!--35--><!--36--><!--37--><!--38--><!--39--></div><div class="index-module_textWrap_3ygOc"><p><span class="bjh-p">在开始十二小时的飞行之前，请检查是否已启用云存储。如果您在Steam上购买了The Witcher 3，则可以像下面这样检查此功能是否已启用：</span></p><!--40--><!--41--><!--42--><!--43--><!--44--><!--45--></div><div class="index-module_textWrap_3ygOc"><p><span class="bjh-ul"><span class="bjh-li"><span class="bjh-p">打开您的Steam库。</span></span><span class="bjh-li"><span class="bjh-p">右键单击“巫师3”，然后从下拉菜单中选择“ <span class="bjh-strong">属性</span> ”。</span></span><span class="bjh-li"><span class="bjh-p">在“ <span class="bjh-strong">更新”</span>选项卡中，确保已选中“ <span class="bjh-strong">启用Steam云同步”</span>。</span></span></span><span class="bjh-p">如果Witcher 3在您的GOG.com帐户上，则过程会稍有不同，但非常简单：</span></p><!--46--><!--47--><!--48--><!--49--><!--50--><!--51--></div><div class="index-module_textWrap_3ygOc"><p><span class="bjh-ul"><span class="bjh-li"><span class="bjh-p">启动GOG Galaxy客户端后，单击左上角的GOG徽标。</span></span><span class="bjh-li"><span class="bjh-p">选择<span class="bjh-strong">设置</span>，然后选择<span class="bjh-strong">功能</span>。</span></span></span><span class="bjh-h3">第二步：转移您的保存</span></p><!--52--><!--53--><!--54--><!--55--><!--56--><!--57--></div><div class="index-module_textWrap_3ygOc"><p><span class="bjh-p">首先，抓住Switch并启动Witcher 3以开始保存转移：</span></p><!--58--><!--59--><!--60--><!--61--><!--62--><!--63--></div><div class="index-module_textWrap_3ygOc"><p><span class="bjh-ul"><span class="bjh-li"><span class="bjh-p">在主菜单中选择“ <span class="bjh-strong">云保存”</span>选项。这会将<span class="bjh-strong">Steam</span>和<span class="bjh-strong">GOG.com</span>都显示为访问保存内容的选项。 </span></span><span class="bjh-li"><span class="bjh-p">选择您拥有的帐户，然后选择您购买的游戏的版本（“ <span class="bjh-strong">标准”</span>或<span class="bjh-strong">“年度最佳游戏”）</span>。 </span></span><span class="bjh-li"><span class="bjh-p">单击<span class="bjh-strong">加载游戏</span>。这将打开Steam或GOG.com的登录屏幕。 </span></span><span class="bjh-li"><span class="bjh-p"><span class="bjh-strong">登录</span>，完成验证码检查，然后填写2FA安全代码。</span></span><span class="bjh-li"><span class="bjh-p">再次选择“ <span class="bjh-strong">加载游戏”</span>以查看可用保存文件的列表。</span></span></span><span class="bjh-p"><span class="bjh-strong">第三步：……然后再次返回</span></span></p><!--64--><!--65--><!--66--><!--67--><!--68--><!--69--></div><div class="index-module_textWrap_3ygOc"><p><span class="bjh-p">无论您是在通勤途中玩过《巫师3》，还是在空中数千英里高空，还是坐在沙发上时，都可以将您的储蓄带回PC上，以体验最精美的游戏。</span></p><!--70--><!--71--><!--72--><!--73--><!--74--><!--75--></div><div class="index-module_textWrap_3ygOc"><p><span class="bjh-ul"><span class="bjh-li"><span class="bjh-p">按下开关上的选项按钮（<span class="bjh-strong">+</span>）以显示菜单栏。</span></span><span class="bjh-li"><span class="bjh-p">从列表中选择“ <span class="bjh-strong">云保存</span> ”。 </span></span><span class="bjh-li"><span class="bjh-p">与以前一样，选择Steam或GOG.com以及您的游戏版本。</span></span><span class="bjh-li"><span class="bjh-p">按上<span class="bjh-strong">载</span>以传输您的保存。 </span></span></span><span class="bjh-p">屏幕底部的一条小通知确认您的保存已上传，表明您已准备好从上次中断的地方接听。 </span></p><!--76--><!--77--><!--78--><!--79--><!--80--><!--81--></div><!--13--><!--82--><!--83--><div class="index-module_mediaWrap_213jB"><div class="index-module_reportContainer_1LjGN"><span>举报/反馈</span></div></div></div>'
        print(html2text.html2text(htm))
        return html2text.html2text(htm)

    @bp.get('/ip')
    def get_ip():
        return Tools.get_machine_ip()

    # @bp.get('/ip')
    # def ip(request:Request):
    #     return Tools.get_ip_description(request)
