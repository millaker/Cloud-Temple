from transitions.extensions import GraphMachine
from utils import is_return, send_text_message, is_passed_roll, send_template_button, send_template_confirm
from utils import send_template_carousel, send_image_url, push_message
from linebot.models import MessageAction, CarouselColumn
import random as rand

meaning = [ 
    "只要太陽出來了，遮蔽天空的烏雲就會隨風而散。 陽光普照大地般地，內心清靜並會充滿光明。 好好努力，會通往成功的道路。只要循著正確的道路，有神明保佑，會平安順心的。",
    "現在正是看眼前的景象的時候。看看花朵含苞待放。如果能夠遇到春天來臨。事情會如花朵綻放般地，能夠擺脫困難，順心吉祥。",
    "勸你定下心來，不要胡思亂想、三心二意了。財富或姻緣等都是是上天注定的。能相互配合，就可以順心如意。等到時機來臨時，就能遇到自己心中所期待的結果（明珠）了。",
    "風平浪靜可以乘船而行。高掛天空的正好是中秋節的又圓又明亮的月亮。不必過多的煩惱和憂慮。福德、財富都是上天注定的，時間一到自然會有好事降臨家中。",
    "未來的前途恐怕會有變化，發生不好的事。勸您先停下目前的計畫，不必急著要搶先機。守在長江岸邊等待時機到來。",
    "雲雨鋒面來了，大雨下個不停。天災發生時，必定會造成損傷。這件事情注定難和諧。更會遇到離家外出的事情。",
    "雲散開就可以看見明亮的月亮。不必問前途要前進或要後退。姻緣是由上天注定好的。如果是上天注定的良緣，做什麼都可以成功。",
    "看見稻子已經結實纍纍。這件事情雙方都會得到答案。安心地在家中等待。妻子、兒女歡樂團員。",
    "龍與虎分屬不同性質的靈獸，相偕住在深山裡。你又何必在背後猜忌，勾心鬥角。卻不知道雖然表面上看起來相親相愛。日後會變成互不相干，形同陌生人的局面。",
    "花開了但是卻只有一半結果，另一半枯萎了。令人惋惜地，你虛度今年的光陰。太陽漸漸地向西山落去。勸你不用再費功夫。",
    "聽到公雞叫，就是要漸漸天亮的時候了。無論什麼事，在子、丑、寅的時候都可以有個結果出現。雲散開了，月亮照耀天下。你就可以平安無事了。",
    "長江的風浪漸漸平息了。現在風平浪靜的時候，船才得以安全的前進。一定會有貴人幫忙。危險的事情轉為平安。",
    "目前遇到了命中注定的難關。雖然盡辦法、費盡心思卻沒有辦法解決。祈求神明也幫忙沒有辦法全然解決難關。這樣的情形就好像要把船航向高灘上一樣困難。",
    "從財運或金錢關係來看，事情漸漸地明朗起來了。就像花開花謝了之後果實結成，有一個結果的時候將要到來。不妨安心地等待月圓時候。這時候到了你便可以平安無事了。",
    "八十歲的高齡才成就事業的是姜太公。晚年才遇到周文王的賞識。目前不用急著問什麼事後事情才可以成功。勸你好好等待運氣來的時候。",
    "不必祈求神明的幫助。也不用費盡心思想要達成所祈求的願望，無論怎麼做總是沒有辦法完成心願。這是因為活在陽世的人沒有辦法瞭解陰間的因果關係。因自己的種種行為而得的果報，這是注定的，一點都由不得現世的人自己作主。",
    "過去重重疊疊的過錯與困難所帶來的傷害，還留在心裡沒有消失，問題的癥結點也尚未解決。就像是家中發生的災禍不是在自己身上發生，但是要提防壞事發生在自己身上一般地，要多做好事為自己造福，這樣可以提防災禍發生。等到龍與蛇交會的時候，所迷惘的事情會有一個結果的。",
    "你要問這件事情的原因與結果。看看有祿馬拱照，前途一片看好。如果有貴人幫忙，可以得到很好發展。結果自然會清清楚楚。",
    "人的一生富貴容華與否，都是命中注定的。如果自己的期望過高或內心驕傲，都會是使你錯過前程時機的因素。不然你還是按照原來的路線發展。等到烏雲散去月亮出來的時候，月亮的光輝會照亮四周。",
    "事業、考試、升官等等都不能得意。只怕命中注定有困難與阻礙。如果做事三心兩意、感情不專等必定會造成自己的損失。勸你不要悲嘆自己時運不佳，暫時放棄往前進的念頭，退守過去的成果。",
    "無邊的佛法神通廣大，誠心地祈求終能得到感應。面臨困難的時候會有不同的遭遇與結果。紅紅的太陽高掛天空照耀。有貴人會來到家裡。",
    "姜太公在八十歲時才有所成就。月亮出來光輝照亮四海。是命中注定的，自然而然會遇到好事。在還沒成功之前暫時住在茅屋裡，總有一天什麼事情都會變得順利的。",
    "想要前往河面寬闊的長江。前途不順利，運氣還沒到來。現在常常手上拿著釣魚線，只怕就像魚遇不到水一樣，白費工夫。",
    "月亮的光輝照亮四海，一片明亮。前途與功名都會化險為夷，不會受影響。遮住月亮的浮雲散去，終會平安無事。神明會保佑，災難不會降臨。",
    "不用費心前途的事情。就算求神問卜也是白費力氣。等到雞犬日過了。不必祈求神明，就可以明白事情的面貌了。",
    "在牡丹中選擇最好的一枝。勸你在花開的時候趕快摘，不要再遲疑了。如果你要問世間的知己在哪裡。做事要趁著春天的時候。",
    "你放寬心情，自由自地生活。家裡平安不用擔心。財寶的事情最後終會轉為順利。不必傷腦筋，也不用求神明幫助。",
    "現在的情況已經不能和以前得意的時候相提並論了。虎落平陽，會被狗欺負。世間的事情很難簡單地說明。就像要越過千山萬水一樣，會歷經種種困難，不遲疑不行吧。",
    "就像是枯了的樹木在還沒遇到春天之前，沒有發芽的機會。目前所祈求的事情的真相還隱藏於黑暗中。不如放寬心不必想要做什麼，等待困難與阻礙過去了。到時候你就可以闖下一片天地。",
    "月亮漸漸地在變化，到了月中就可以看到圓滿的月亮。但是月中過後，月亮由圓轉缺，所以做事要防範志得意滿、心高氣傲帶來的損失。自我檢討，好好調整自己，才能迎向美好前途發展（擺臭臉是不行的）。如果自己不好好改變，依然故我，這樣必定會做事白費力氣。",
    "現在就好比正是柳樹綠油油的時候。也是你發揮所長，創下一番天地的時候。就像樹木開花之後結果了，過去辛勤的付出會有收穫，沒有白費力氣。福與祿會自然到家門來。",
    "龍與虎在門前相遇了，但彼此性質不同（個性不合）。事情的結果必定和龍虎相爭有關。原本龍與虎都是神獸，但是相互爭鬥之下，就像黃金變成鐵，失去原本的價值。東西已經失去原本的價值，沒有必要再問神明的旨意或祈求神明幫忙了。",
    "想要渡過河面寬闊的長江。要乘風駕船而過，但是風還沒吹起，不能吹動船帆，不是行船的時候。在家中好好用心準備，祈禱神明幫忙。時機到了，猶如魚得到水一樣。",
    "這是一條要走盡危險的高山的路。不要嫌棄這條路有重重的困難。如果看到蘭花桂花漸漸開的時候。 就算是蛇也會化身成龍，就是成功的時候了。（蛇只能在地面蛇行，但龍可以飛天）",
    "這件事情不必費心思考。事情改變了，自己心裡自然會知道。未來會有事情和諧的一天。漸漸地從危險中脫出，會平安無事。",
    "福如東海一樣寬廣，壽如山一樣高。你何必嘆息自己遭遇苦難呢。命中有福氣，自然能夠逢凶化吉。祈求神明的保佑，自然就會得到保佑，平安無事。",
    "運氣來了，做事得意，身份地位也會變得顯要。你現在所做的事情都是好的，對別人也有好處。未來沒有什麼可以難得倒你的。作下好的決定，神明也會保佑你。",
    "想要出人頭地，就要守著正道而行。即使不向神明祈求保佑，也能心安理得。就像看著日出日落，發現天地運行的道理。按照道理而行，就可以成功。",
    "如果要請神明指點未來的道路。勸你暫時放下心願，改用欣賞高樓的心情，看待這件事。安心地過生活，等待下次的機會。必定會有貴人來幫助你。",
    "人一生的富貴、功名都是天生注定的。如果天生富貴，自然會讓你光耀門楣。這件事情對你不會造成損害。有緣結為夫妻，就能一生歡喜相隨。",
    "事情到現在這樣的狀況，自己也很難推辭與自己無關。就像是在歌唱歡樂的情境中，卻自己一人獨自猶豫徘徊。聽到雞犬的聲音，代表著將傳來事情的消息。如果是夙世的姻緣，自然會在一起。",
    "所計畫著要前往的方向，就像是要渡過江水之後又要爬過高山，有著重重的困難。這些困難是誰也無法預先知道的。如果照著原先的想法繼續下去，無論如何努力終究還是沒有辦法順利渡過難關。紛紛擾擾的事情會持續著，讓人不得安寧。",
    "這一年做事相當急躁。你應該要放下急躁與猶豫的心情，定下心來。你所祈求的事情會有貴人幫助你，但是目前貴人還在遠處沒有出現。等到月中的時候，你所祈求的事情就會漸漸得到消息。",
    "客人到了，是前途發展，可以獲得利益的象徵。你必還在猶豫猜測呢。雖然事情進行才到一半遇到阻礙或遲疑。等到月亮出來了光輝照耀，這時候就是你運氣到了的時候。",
    "花開了之後，現在已經結成果實了。富貴容華會伴隨到老。君子與小人相見面，君子要包容體諒，雙方好好相處。事情會平順發展，不要煩惱。",
    "努力的話就會功成名就，讓你的名聲彰顯。前途平順，能夠得到富貴容華。就像是遇到的月光照耀一樣。十五滿月又圓又亮，照得滿天光輝。",
    "你何必要問神明是否可以顯現神威幫助你呢。捫心自問什麼對你是好的、有幫助的，選擇對自己有利的方向。你等到月中旬的時候。這件事情可以脫離危險局面，由凶轉吉。",
    "在人世間作事情與他人意見不相同。就像雲遮住月亮，看不太清楚般地。還看不到你心中想要前往的未來。因為時機未到，還不是你發揮的時候。",
    "別人告訴你的很多話，不要隨便相信。風雲未起，不是龍（你）發揮的時候。你目前雖然人身在暗處，但是已經得到一點點訊息了，根據這個訊息其實你已經知道要怎麼做了。既然知道了，你又何必一再地問神明的意思呢。",
    "向菩薩、神明發誓會堅持到底，不改變心意地持續下去的話。就可以得到前途光明的好消息。雖然這件東西目前僅僅是鐵而已。因為你的努力，鐵也可以變成黃金。",
    "無論向東西南北的哪一個方向，都不能走。前途正是面臨困難的時候。勸你定下心來，不要再煩惱。神明會保佑你家裡平安和樂的。",
    "功名與事業的成就都是上天注定的。目前不用對祈求的事情每天掛心煩惱。如果想問祈求的事情的結果會如何。這件事情很快地就會有個結果。",
    "你來問心中的疑問。是行善的人家，自然會有福報。運氣與財運兩者都亨通。有朝一日喜氣會充滿你的家門。",
    "就像一盞燈孤孤單單地在寂靜地黑夜中亮著，雖然身在黑暗中但是還有一絲光芒。所祈求的願望會平安無事，不會發生什麼不好的事情。如果做事能夠好好努力累積成果，或平日多行善事累積善緣。你的心願會傳達神明，得到庇佑。",
    "要知道現在想要做的計畫，都是不切實際的。看看前途昏暗，做事未必可以成功。即使身上依然還藏著寶石碧玉，沒有改變。但是珠寶只是藏於自己的心中，還沒被發覺，這是沒有用的事情。",
    "就像人生病的時候，還要顧慮周圍的事情， 沒有辦法全部照顧周全的。事情過了，就不要再去問事情的前因後果。過去的事情留在心裡，也只是讓自己心裡難過而已。",
    "勸你不要慌張，把心定下來。運氣來的時候，前途就會平順。眼前沒有什麼大事情。又有神明保佑你可以安心地過生活。",
    "猶如蛇想要變成龍，想要有所成就。只怕命中注定的運氣尚未到來。就像長期生病，身體虛弱，不妨坐著安心養病。雖然很多人告訴你怎麼做比較好，但是不可以隨便相信。",
    "有心要做善事不要遲疑，趕快去做。想要求名聲顯現，現在正是時候。內心想完成的事情必定可以得到認同，處理得宜。就像想獲得財寶自然而然就可以得到一樣，心願得以完成。",
    "當月亮出來的時候光輝照耀四周，事情也會順利吉祥。但是浮雲總有遮住月色的時候。在家好好用心再做準備。當機會來的時候，將會有幫助。",
    "本籤為頭籤，等於是拔得頭籌，幸運有嘉，風雲際會。天上聖母告示弟子說：能得此頭籤絕對百事良吉，萬般皆如意，添油、添香更可以大吉昌。當然油香是隨君之能力，心意去決定。既然是百事良吉，萬般均如意，富貴又可福壽綿長，人生的三大願望都接踵而來，在此良好的際遇裡，更應時時警惕，勿忘再修身、積德、或着是佈施、行善、救濟等。",
    "百事皆吉 求財大利 耕作大收 經商有利 家運平安 運途好 功名有望 婚姻可成"
]
explanation = [ 
    "抽得此籤表示所問之事目前面臨著阻礙與困難，但是就像雲會散開，陽光會出來，事情的陰霾會掃去，而且神明會保佑，事情最後會平安順利的。",
    "目前的處境猶如春天來之前的寒冬，雖然有種種磨難，但是以前的努力已經快要有成果了，只要繼續努力，會擺脫難關，成功時機會到來的。",
    "目前處於搖擺不定、心意難安的局面。其實財富或緣分是上天注定好的，該是你的就會是你的，一定要有決心，選擇好方向誠心誠意、專心一致地努力，最後會得到您想要結果。 若問感情得此籤，表示雖然目前和對方有許多的問題與阻礙，即使有分手之虞，但是若能雙方相互配合，專情、努力不放棄這段感情，最後會有情人終成眷屬。若已分手問復合，需雙方能檢討分手原因，能相互配合則復合可成。",
    "求得此籤表示您目前的情況相當平靜無事，不必過多猜疑、自尋煩惱，事情順利進行著。若問事情成功時機為中秋。",
    "雖然計畫很好，但是一旦執行會有意想之外的壞事發生，自己的運氣亦走到不好的時候，要小心為宜。幸好有太白金星守護，不會發生什麼大壞事，還是守住目前的的成果，等待時機來了，再做計畫。",
    "所謂「生死有命，富貴在天」，「姻緣天注定」，您得到此籤表示您所有請示的事情是命中所沒有的，就算勉強爭取也不會得到好結果，猶如天災來臨一定會有所損傷一樣，這件事求強會對您造成傷害。也要留意會有發生離家赴外地的事，或者是放棄原本的成果之意。求得此籤應避免與人合作。",
    "雖然目前您所問的事情遇到一些困難或麻煩之處，而且你已經清楚的知道這件事情的問題所在了。不用擔心地問現在是要往前進還是要往後退，而是認清事情的真相，按照道理來做事情。只要是上天注定的好姻緣或機會，做什麼都會順利成功的，如果不是天定的良緣，也不要強求。",
    "看見結實纍纍的稻子，表示所詢問的事情已經得到消息，要認同並接受這樣的結果。若問感情，交往中感情穩定者表，示未來有情人終成眷屬，或有得子之兆；若分手問復合者，「此事必定兩相全」，若一方以無意復合，則復合難成，應該平心靜氣接受這樣的結果。",
    "「龍虎」有激烈鬥爭之意，意寓兩者本質不同，不要勉強相處，即使目前情況看起來相處愉快或前景看好，但是日後會鬧得不愉快，最後形同陌路。求得此籤舉凡男女交往、結婚、合夥做生意等皆不宜，最後會不愉快地分手或拆夥。",
    "雖然自己努力與用心，但是目前的氣運就像是太陽西下一樣往下走，漸漸變暗，即使努力也大多白費力氣，沒什麼成果，只能感嘆與惋惜浪費時間，所以不必想要達成心中的願望，或做改變。問交往、結婚，此對象不宜。問換工作，則應於原來的工作崗位上繼續努力，不宜換。",
    "當雞啼叫就是即將天亮的時候，雖然現在您所問的事情如黎明前的黑暗，還不明朗，也像雲遮住月亮的光輝般地昏暗，但是等到時機（子、丑、寅）一到，就像是陰霾掃盡，月亮放光明照耀天下一樣，結果顯現出來。由於結果是「見太平」，是平安無事的意思。若問考試需要努力，可以考上但是成績不是非常高。問事成時機的話，子、丑、寅近的話可解為月份，月份多為農曆之十一、十二、一月，也有應於國曆一、二、三月的情況，遠可解為鼠、牛、虎年。籤詩中的「靈雞」可視為契機或者是貴人之意，如為貴人時可留意身邊屬雞的的人，可能就是您的貴人。",
    "危險的事情終於在貴人的相助之下，可以轉為平安，就像長江的風浪平息了，船才得以安全的前進。求得此籤表示所期待的事面臨危險的狀況，必須忍耐並等待貴人相助才能夠解決，或找尋貴人幫忙化解危機。抽到此籤最重要的事要分辨對自己而言危險指的是什麼，例如很多人為求感情復合，都求到此籤，但卻未必能復合，這是因為有些人的對象是不好的對象，分開對他而言才是脫離難關，邁向平順的未來。若分手的對象是良緣，復合的方法應該要找他人（貴人）從中協調，復合有望。",
    "所詢問之事，因為是命中注定會遇到的難關，所以無法如願完成，即使強求或求神明保佑也無法完成心願。籤詩故事「撐渡伯行舟遇太歲」，求籤者當注意自己是否剛好處於太歲年，應該要祭太歲星君化解而沒有做。",
    "這首籤詩最重要的事要瞭解「結子成」的意思，表示所詢問的這件事情已經有了一個結果了，這個結果在農曆十五或中秋節的時候就可以看出來。月中桂指的是月圓的時候，或中秋節，求得此籤所詢問的問題要到農曆十五或中秋節才能平安度過。由於籤詩中最後的結果是「太平」，所以表示在太平之前是有困難與磨難，而這個困難要特別留意與金錢有關，因為籤詩指點「財中漸漸見分明」，困難結束之後也只是平安無事而已。",
    "就像姜太公八十歲才遇到周文王，你先不用著急詢問目前的這件事情，不要嫌棄運勢晚成，勸你守著目前的狀況，等待時機到來。目前時運未通，應該靜守目前情況，不宜做改變。若問姻緣，則緣分尚未到來。問換工作亦不宜。問疾病，恐會拖延。",
    "心願無法達成，這是因為自己所不知道的因果關係，因此現在的種種不順遂，不要怨天尤人。做事要心存善念，尋正道而行，盡自己的本分多做好事，努力積善因，未來才有結善果的機會。",
    "這首籤詩提醒當事人要改進過去的錯誤，雖然這個錯誤對自己還沒有造成什麼影響，但是也要多做好事、認真做好自己的分內工作，真相大白或事情得到結果的時機在龍蛇交會之時。龍蛇交會所指的是事情明朗、結果出現的時機，近者指月份，龍（辰）為三月，蛇（巳）為四月，遠者指龍年與蛇年交接的時候。但若求籤者的生肖為龍或蛇之一，也不妨思考是否龍與蛇指的是當事人與所求之事或貴人為另一生肖。",
    "你想問的事情需要有貴人相助，只要有貴人相助，會有好結果。籤詩中「祿馬」拱前程，也不妨思考自己的貴人是否與馬字有關，例如姓馬或生肖屬馬，或者應徵求職的公司與馬有關。「祿馬」之馬字亦有解為農曆五月之意，若不作貴人解時，可參考事成之時為五月。祿馬是古代狀元所騎的馬，意指得到功名祿位，所以若問考試則有高中之意。若猶豫找工作或考公職，則可朝公職發展。",
    "人的一生會有多少榮華富貴都是早已注定好的，如果自己心裡的期望過高，一直努力追求沒有辦法達成目標，這樣做反而會錯過原本屬於你的前程與機會。目前所求的事情有阻礙，就像烏雲遮住月亮看不清楚方向般地，不利於現在做改變，暫時還是按照目前的樣子，按兵不動。在等待機會來臨之前，應該要先自我檢討，自我修正與充實，機會一來，就像等到月亮一出來，光輝照耀四周明亮般地，你就會清楚未來的方向了。抽中此籤，要特別留意勿心高氣傲、得理不饒人或訂定目標過高超過自己的能力範圍，要衡量自己的條件或情況，作自我調整，當機會來了，才不會錯過屬於自己成功的機會。",
    "目前遇到的難關是命中注定的，不需要嘆氣悲傷，暫時退守目前的狀況，不要改變。抽到此籤要特別應注意「退」這個字，這是神明指點所遇難關的的解決之道。例如官司不宜纏訟、宜和解，此即為「退」。常有問健康的信眾抽中此籤，「只恐命內有交加」表示恐怕會危及生命，要小心提防。生病時當然是要看醫生，不過若有無法醫治或診治的疾病，在此提醒籤詩中「兩家」有時暗指兩家先人的問題，也就是常見的雙姓祖先。",
    "如果誠心誠意懇求神明與菩薩的幫忙，神明會感受到你的誠心幫助你渡過難關。這與沒有神明的幫忙時，遭遇困難的境遇是很不相同地。有神明的幫助，可以逢凶化吉，神明的力量就像日正當中的陽光照耀四周一樣，光明無比會庇佑誠心祈願的你，而且還會有貴人幫助你渡過難關。抽重此籤當誠心誠意像神明祈求幫助，若得到神明應允，就可以感應到無邊的神力幫助，還會引導貴人協助你你完成心願。不過既然是懇求神明的幫助，完成心願時可別忘記要向神明感恩還願。一般籤詩常見「月出光輝」，而此首籤詩是「紅日當空」，其光亮程度的差異巨大，所以佛法靈通的力量怎容輕視。",
    "這首籤詩勉勵當事人不要擔心時運不佳、運勢晚成，像姜太公在八十幾歲才得到文王的賞識，所以雖然事業晚成，但只要等待自己時運的到來，自然就會像會像月亮出來，四處充滿光輝般地，前途光明。目前求籤者的情形則是「茅屋中間」，就像住在茅屋中般地清貧，安貧樂道、清心寡欲是目前處事的方法，等到時機到來，自然而然會有所成就。",
    "目前的前途與運勢不好，就像要去廣闊的長江，但是卻沒有辦法到達，既然不能到長江，即使有釣竿在手，恐怕也釣不到魚。所以向神明所詢問的事情不是自己可以發揮的機會。「如魚得水」是劉備得諸葛孔明為軍師時，向關張二結義兄弟說明自己得以抒發志向的心情，此籤「魚水不相逢」表示即使有著才能或有意發展，但還沒有到達發揮的餘地，只能靜心等待時機的到來。問感情，表示目前這個人不是自己的良緣對象。",
    "目前雖然遇到困難，但是有神明保佑災禍不會降臨的，最後就像遮住月亮的浮雲散去了，月光照亮四處般地，困難得以化解，前途和官位都可以化險為夷，平安無事。這首籤詩為先經歷險境，後因神明保佑得以平安脫險若問時機為「月出」，指農曆十五或中秋。但也可朝向遇女性貴人困難得解的方向思考。",
    "對於所求的事情不用費心求神，這件事「雞犬日」之後，就可以明白事情真相或結果了。雞犬就是酉戌，可以做時、日、月、年解，時是酉時（下午五至七點）、戌時（下午七至九點），日的話可對照農民曆查詢，月份就是指農曆的八、九月，若為年份就是雞、狗年。",
    "春天是牡丹花開的時候，所以要摘牡丹花要趁著春天花開的時候，如果錯過時機就沒有花可以摘了，所以求籤者要問的事情，就像摘取最美的牡丹花一樣，要趁著春天來的時機進行。",
    "順應環境變化，不要強求，安心守分地過生活，這樣做不會對自己造成損傷，所以不必費心向神佛祈求願望實現，只要是命中該你得到的東西，自然會得到。",
    "現在正是運氣不佳的時候，與過去的風光歲月不能相提並論，就像勇猛的老虎落難也會被狗欺負，世間的事情很難簡單地說清楚，目前想做的事情如果做了會歷經種種困難會被欺負，所以還是放棄吧。目前不適合遠行或做改變。",
    "此籤表示當事人的時運未至、且對於事情的真相不明，就像樹木處於寒冷的冬天，還不是發芽的時候，此時不適合貿然做決定或改變，靜心等待時機到來，到時候可以有一番作為。時不我與，不適合做任何新計畫或改變。",
    "月亮的陰晴圓缺是固定的道理，人也是一樣，驕傲自滿則會招致失敗，所以求得此籤當要注意自己的言行舉止，要謙虛待人，才能避免失去目前的成果。如果不知修正自己，未來將會勞心勞力卻沒有成果。此籤有運勢正好的時機將去，未來做事不能再靠運氣了，當事人要自己努力才能挽回頹勢，如果還是按照目前的作法，將會徒勞無功。",
    "得此籤表示正是發揮長才，只要好好努力會得到好的結果。所祈求的願望努力可以實現",
    "龍虎交會表示有相互爭鬥之意，所求籤詢問的這件事情必定與相互爭鬥之事有關，因為不合，造成目前所期望的事情失去了原來的價值（黃金變鐵，變不值錢了），問題的根源其實當事人自己也已經知道了，不必費心在在詢問神明了。經常有人問感情求得此籤，籤意表示兩人個性不合，致使感情變質。亦有詢問工作關係改善的，表示需調整自己為人處事的態度，勿強出頭。",
    "你目前時運不佳，還沒辦法達成心願，好好準備與充實自己，時機到的時候，就像風來了，帆船可以渡過長江，你也會像魚得到水一樣，可以發揮自己的長才。目前要在家好好自我檢討與自我改進，神明會保佑你，發揮自己才能的一天會到來。此籤「再作福」，有第一次事情不會成之意，要檢討失敗原因，加以改進，再次努力神明相助事情會成之意。",
    "雖然目前面臨種種困難，但是千萬不要嫌棄，只要等到蘭花、桂花開的時候，就是你渡過難關，邁向成功的時候。若問時機，可以「蘭桂」來解時機。雖然蘭花因品種不同開花時間不同，但是傳統上常稱「春蘭」，所以蘭花的季節可視為春天。桂花的花季為春、秋二季，所以此籤提示的時機以春為重、秋為輔。另外「若見蘭桂漸漸發」，是此籤提示事情成功的契機，除了解為時間之外，得籤者，不妨想想所求之事是否有與「蘭」或「桂」二字相關的事、人或公司名等，這可能是事情解決的契機。蘭常比喻君子，桂常比喻貴人，因此蘭桂可能比喻君子一般的貴人。",
    "心中所想要祈求的事情不必再費盡心思想要實現，事情改變了，其實自己心裡也知道，不必強求了。看看未來會有平順的時候，那才是屬於你發揮的時候，屆時你會漸漸脫離目前危險的局面，平安無事的。",
    "你是個有福氣的人，雖然遇到困難，誠心祈求神明保佑，事情會逢凶化吉，平安無事的。",
    "現在正是運氣好，適合大展伸手的時候，只要作下對自己與別人都好的決定，什麼事情都不能阻礙你成功，而且神明也會保佑你順利。",
    "這首籤詩指點事情成功的關鍵在於「在中央」，也就是要按照道理而行。人生難免就像每天日出日落一樣，有好時、有時壞，輪流而來，但是只要按照做人的道理做事，謹守自己的本分繼續努力下去，每天可以過得心安理得，而且也會有成功的一天。「在中央」提示事情的重點，舉例來說，如果公務人員問職務調動，則中央單位為佳；若一般人職務調動，則總公司權力核心所在地為佳；買屋則鬧區優於郊區。",
    "目前所其期待的事情不是你的機會，放下追求這的機會的心，改以遠觀欣賞的心情看待這件事，安心地等待屬於自己的機會，有一天必定會有貴人幫助你完成屬於你的成功。",
    "人一生中的富貴、功名與姻緣命中自有定數，若是你的自然可以得到，若不是你的強求也不能得到。你心中祈求的事情對你不會造成什麼損失，你終會得到屬於你命中注定的緣分，歡喜過人生。",
    "目前求籤者處於由於徘徊未定的局面，而這樣的狀況與自己過去的作為有關，應當檢討自己的錯誤加以改進，若要看事情的轉機要等到「雞犬相聞」的時候，會有明確的消息出現，就像若是注定的姻緣，自然而然結婚一樣。「雞犬相聞」，出自陶淵明的桃花園記，原本是指雞與犬和諧相處，這首籤詩中除了和諧意之外，尚含有指點時機之意，雞為酉、狗為戌，日為酉戌日、月為農曆八、九月、年為雞狗年，是成事的好時機。若問人際關係或感情復合，則必須注意與對分相處和諧才是成事之道。",
    "抽到此籤表示若按照心裡想的方向進行，困難重重將無可避免，而且無法預知。當虛心檢視自我，擇善而行，甚至要放棄原先的想法為宜。人越是在困難的時候，越要堅守自己的本分，好好做事，廣結善緣，才不至於兇事因自己的不慎變得更糟。",
    "雖然你急切的想要達成心願，但是一直沒有達成，你不要因此急躁與猶豫，要定下心來，雖然幫助你的貴人還在遙遠處沒到來，但是過了月中之後，你會漸漸得到好消息。這首籤詩表示自己發揮的時機未到，就算著急也沒有用，當靜心等待時機與貴人的幫忙。月中通常是指農曆十五，不過也不能排除國曆。",
    "現在已經是有結果與收穫的時候了，你不必猜疑，雖然這件事情還有著一些阻礙或猶豫，但是堅持下去，你會雲開見月，前途光亮。「客到」可以解作客人到了、求籤者、或者是到外地發展的意思。「月出」是事情得解的徵兆，若為時機則在「月出」，農曆十五或中秋之意。",
    "得此籤表示，目前這件事情的結果已經出現了，這個結果會伴隨著你到老，你就高興地接受，不要在為這件事情煩惱了。籤詩中「君子小人相會合」是指籤詩故事孔夫子過番逢小兒，意指所遇之人有不明理的地方或喜歡強詞奪理，要體諒、禮讓彼此好好相處。「小人」亦有指小孩的意思，女性得此籤，可能有懷孕得子之兆。",
    "得此籤表示所求知之事，經過一番努力，心願可以完成。像是月亮的光輝般地照耀，也意指著雖然明亮，畢竟還是晚上的光輝，所以如果是問考試，必須苦心用功可以考上，但卻未必是高分考上。若問事情成熟時機，為農曆十五或中秋之時。",
    "你何必要問神明的意思呢，其實你心中對事情的好壞很清楚，要選擇對自己有利的方向，所祈求的事情到月中旬的時候，可以脫離困難危險的狀況，變往好的的方向發展。籤詩「自己心中皆有益」指點的事化解危險的方法。所祈求的事情，要自己想清楚選擇對自己有利的方向，這樣才可以讓自己趨吉避凶。 而「月中旬」是只事情的解決時機，中旬就是十日到二十日。",
    "因為與人不合且時機未到，未來一片黑暗，所以現在不宜做新的嘗試，守著目前的狀況為佳，例如換工作等不宜。所求之事與人有關者，表示與這人心意不相通、看法不一致，事情無法如願達成。",
    "抽到此籤表示陷入被欺瞞或迷惘的狀況，對方或身邊的人告訴你很多事情，你不要隨便相信，應該要自己明辨是非，根據正確道理來決定自己的方向。",
    "所謂精誠所至金石為開。所祈求的事情目前的狀況好比只是鐵而已，要靠自己堅定的意志，不斷地努力之下，才有機會讓事情好轉成功（鐵變成金）。求得此籤表示，所祈求的事情需要歷經阻礙，而且在過程中，得籤者可能會有意志動搖想放棄的時候，所以當你要向祈求神明幫忙時，神明要你先確定自己是否有堅定的決心與毅力，如果確認自己有絕不改變決心，會堅持到持續不斷努力下去，會有好消息，而且神明會幫助你的。",
    "所期望的事情就像是無論要往東南西北哪一個方向前進，都是不可行的，現在先放下所祈求的事，安定自己的心情不要在煩惱了，這樣做神明會保佑讓你家裡平安和樂。外出、異動都不宜。如求籤者面臨多選一時，可參考「東西南北不可行」，名字中有東西南北的不要。",
    "功名與事業都是上天注定的，該是你的總會屬於你，但是若不是你的不必強求，只要盡自己的努力去做就好了，目前不用對祈求的事情每天掛心煩惱，如果想問祈求的事情的結果會如何，這件事情很快地就會有結果了。",
    "得此籤表示運氣已經開始好轉，多做善事，運氣與錢財這兩件喜事將會臨門。問婚姻、求子或感情者，財子除了解做錢財之外，也有有懷孕生子之意。",
    "目前雖然孤單寂寞或孤立無援，但是平日就要多努力、多做好事，這樣可以為自己的成功累積善因，只要你有努力，神明會聽到你的心願，保佑你。正所謂天助自助，事情成功與否，端看自己的努力，外加神明的護持，才會成功。",
    "就像寶玉藏於石中，需要經過琢磨，才能顯現最美好的價值一樣，現在你還處於磨練的時候，要多充實自己，並將自己的缺點加以修正，不然只因為一些小小的缺點，遮蔽你的優點與才能，讓自己無法實現願望，導致所作所為只是徒勞無功。此籤為懷才不遇、時不我與之籤，還是靜靜等待可以發揮的時機吧。「看看發暗未必全」亦有自己身處在暗處，或對於事情的真相沒有全部瞭解，因為對事情不瞭解（事情不是你想的那樣），所以根據非事情所訂的計畫，想要實現不過是白費力氣吧。",
    "不必再費心想要問這件事情的因果關係，過去的事就讓發過去吧！忘記吧！老是想著這件事情，讓這件事情繼續留在心中，就像生病的人，沒有辦法做好事情的，對自己沒有好處，反而只是讓你心裡難過，於事無補。若問健康，因「病中若得苦心勞」，疾病恐怕變重、拖長，要小心醫治。",
    "雖然目前有點猶豫不知所措，但是不必慌張，你的運氣即將來臨。等運氣來了，一切都會順利吉祥。在運氣到來之前，也不用擔心，不會發生什麼有損害的事，而且神明也會保佑你，安心過生活吧。",
    "雖然想要完成願望，但是恐怕自己的運氣未到，沒辦法完成。就像長久生病身體不適合勞累，你何不先放下目前的計畫，安心調整自己與等待時機。由於現在不是你可以發揮的時候，不要輕易相信別人（對方）告訴你的話，而照著做。凡事以不動對應。",
    "因為平時多做善事，想要完成心願時，就能神明保佑，能自然而地得到財寶（完成心願）。",
    "運氣來的事後就像在月亮出來的時候，光輝照耀，做事順利。但是月亮的光輝也有被雲遮住的時候，在這個時候時運不濟，需要自我反省檢討、多充實自己、多做好事，這樣當機會來臨的時候，你平日的累積將會幫助你成功。此籤中「戶內」二字，所以欲離家外出發展者不宜。「再作福」有第一次未能成功，需要再次努力的意涵。",
    "已解釋",
    "已解釋",
]
class TocMachine(GraphMachine):
    server_url = "https://d947-58-114-82-32.jp.ngrok.io"
    static_folder = "/assets/img/"
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.diceroll = -1
        self.card = 0

    # Transition conditions
    def is_going_to_history(self, event):
        text = event.message.text
        if is_return(text):
            return False
        if text != "history":
            return False
        return True
    
    def is_going_to_donate(self, event):
        text = event.message.text
        if is_return(text):
            return False
        if text != "donate":
            return False
        return True

    def is_going_to_Door(self, event):
        text = event.message.text
        if is_return(text):
            return False
        if text != "visit":
            return False
        return True
    def is_going_to_Meditation(self, event):
        text = event.message.text
        if is_return(text):
            return False
        if text != "pray":
            return False
        return True
    def is_going_to_Start(self, event):
        text = event.message.text
        if is_return(text):
            return False
        if text != "draw":
            return False
        return True
    def is_going_to_Dice(self, event):
        text = event.message.text
        if is_return(text):
            return False
        if text != "cast":
            return False
        if not is_passed_roll(self.diceroll):
            return False
        return True
    def is_going_to_Result(self, event):
        text = event.message.text
        if is_return(text):
            return False
        if text != "reveal":
            return False
        return True
    def is_going_to_Meaning(self, event):
        text = event.message.text
        if is_return(text):
            return False
        if text != "translate":
            return False
        return True
    def is_going_to_Explanation(self, event):
        text = event.message.text
        if is_return(text):
            return False
        if text != "explain":
            return False
        return True
    def is_going_to_Main(self, event):
        return True
    # Function called on entering a new state
    def on_enter_Main(self, event):
        send_text_message(event.reply_token, \
        "歡迎來到雲端神廟\n" + \
        "輸入 history 查看廟宇歷史\n" +\
        "輸入 visit 參拜\n" + \
        "輸入 donate 來幫助我們\n" + \
        "過程隨時可以輸入 return 返回主頁")

    def on_enter_history(self, event):
        send_text_message(event.reply_token, "Entering history, return to return")

    def on_enter_donate(self, event):
        send_image_url(event.reply_token, self.server_url + self.static_folder + "donation_box.jpg")
        push_message(event.source.user_id, "請考慮幫我們維護")
    def on_enter_Door(self, event):
        send_image_url(event.reply_token, self.server_url + self.static_folder + "door.jpg")
        push_message(event.source.user_id, "輸入 pray 開始參拜")

    def on_enter_Meditation(self, event):
        send_template_confirm(
            event.reply_token,
            "Meditate",
            "在心中默念自己問題",
            [ 
                MessageAction(
                    label = "抽籤",
                    text = "draw"
                ),
                MessageAction(
                    label = "返回主頁",
                    text = "return"
                )
            ]
        )

    def on_enter_Start(self, event):
        self.diceroll = rand.randint(1, 6)
        self.card = rand.randint(1, 62)

        send_text_message(event.reply_token, "來看看這張籤是不是屬於你的 輸入 cast 擲筊")

    def on_enter_DiceOne(self, event):
        num = rand.randint(1, 6)
        self.diceroll = num
        send_image_url(event.reply_token, self.server_url + self.static_folder + "success.jpg")
        push_message(event.source.user_id, "成功 還要成功兩次，輸入 cast 再擲一次")

    def on_enter_DiceTwo(self, event):
        num = rand.randint(1, 6)
        self.diceroll = num
        send_image_url(event.reply_token, self.server_url + self.static_folder + "success.jpg")
        push_message(event.source.user_id, "成功 還要成功一次")

    def on_enter_DiceThree(self, event):
        num = rand.randint(1, 6)
        self.diceroll = num
        send_image_url(event.reply_token, self.server_url + self.static_folder + "success.jpg")
        push_message(event.source.user_id, "成功 輸入 reveal 來看抽籤結果")

    def on_enter_Result(self, event):
        send_image_url(event.reply_token, self.server_url + self.static_folder + "card" + str(self.card) + ".jpg")
        push_message(event.source.user_id, "輸入 translate 看籤詩語意")

    def on_enter_Meaning(self, event):
        send_text_message(event.reply_token, meaning[self.card - 1] + "輸入 explain 來解籤")

    def on_enter_Explanation(self, event):
        send_text_message(event.reply_token, explanation[self.card - 1] + "輸入任何東西回到主頁")

    def on_enter_Fail(self, event):
        num = rand.randint(1,2)
        send_image_url(event.reply_token, self.server_url + self.static_folder + "fail" + str(num) + ".jpg")
        push_message(event.source.user_id, "這張好像不是我們要的，輸入 draw 重新抽籤")

