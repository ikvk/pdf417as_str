import math


def encode(string, columns=-1, security=-1):
    """
    :param string: str, string to encode
    :param columns: int, number of data columns, (columns < 1 - auto)
    :param security: int, security level, (security < 1 - auto)
    :return: bar code text for pdf417 font
    """
    # Tables
    # This string describe the ascii code for the "text" mode.
    # ascii contain 95 fields of 4 digits which correspond to char. Ascii values 32 to 126. These fields are:
    # 2 digits indicating the table(s) (1 or several) where this char is located. (Table numbers : 1, 2, 4 and 8)
    # 2 digits indicating the char. number in the table
    # Sample : 0726 at the beginning of the string : The Char, having code 32 is in the tables 1, 2 and 4 at row 26
    ascii_codes = "07260810082004151218042104100828082308241222042012131216121712190400040104020403040404050406040704" \
                  "08040912140800080104230802082508030100010101020103010401050106010701080109011001110112011301140115" \
                  "01160117011801190120012101220123012401250804080508060424080708080200020102020203020402050206020702" \
                  "08020902100211021202130214021502160217021802190220022102220223022402250826082108270809"

    # 8 strings describing the factors of the polynomial equations for the reed Solomon codes.
    coef_rs = [
        "027917",
        "522568723809",
        "237308436284646653428379",
        "274562232755599524801132295116442428295042176065",
        "361575922525176586640321536742677742687284193517273494263147593800571320803133231390685330063410",

        "539422006093862771453106610287107505733877381612723476462172430609858822543376511400672762283184440035519031" +
        "460594225535517352605158651201488502648733717083404097280771840629004381843623264543",

        "521310864547858580296379053779897444400925749415822093217208928244583620246148447631292908490704516258457907" +
        "594723674292272096684432686606860569193219129186236287192775278173040379712463646776171491297763156732095270" +
        "447090507048228821808898784663627378382262380602754336089614087432670616157374242726600269375898845454354130" +
        "814587804034211330539297827865037517834315550086801004108539",

        "524894075766882857074204082586708250905786138720858194311913275190375850438733194280201280828757710814919089" +
        "068569011204796605540913801700799137439418592668353859370694325240216257284549209884315070329793490274877162" +
        "749812684461334376849521307291803712019358399908103511051008517225289470637731066255917269463830730433848585" +
        "136538906090002290743199655903329049802580355588188462010134628320479130739071263318374601192605142673687234" +
        "722384177752607640455193689707805641048060732621895544261852655309697755756060231773434421726528503118049795" +
        "032144500238836394280566319009647550073914342126032681331792620060609441180791893754605383228749760213054297" +
        "134054834299922191910532609829189020167029872449083402041656505579481173404251688095497555642543307159924558" +
        "648055497010",

        "352077373504035599428207409574118498285380350492197265920155914299229643294871306088087193352781846075327520" +
        "435543203666249346781621640268794534539781408390644102476499290632545037858916552041542289122272383800485098" +
        "752472761107784860658741290204681407855085099062482180020297451593913142808684287536561076653899729567744390" +
        "513192516258240518794395768848051610384168190826328596786303570381415641156237151429531207676710089168304402" +
        "040708575162864229065861841512164477221092358785288357850836827736707094008494114521002499851543152729771095" +
        "248361578323856797289051684466533820669045902452167342244173035463651051699591452578037124298332552043427119" +
        "662777475850764364578911283711472420245288594394511327589777699688043408842383721521560644714559062145873663" +
        "713159672729624059193417158209563564343693109608563365181772677310248353708410579870617841632860289536035777" +
        "618586424833077597346269757632695751331247184045787680018066407369054492228613830922437519644905789420305441" +
        "207300892827141537381662513056252341242797838837720224307631061087560310756665397808851309473795378031647915" +
        "459806590731425216548249321881699535673782210815905303843922281073469791660162498308155422907817187062016425" +
        "535336286437375273610296183923116667751353062366691379687842037357720742330005039923311424242749321054669316" +
        "342299534105667488640672576540316486721610046656447171616464190531297321762752533175134014381433717045111020" +
        "596284736138646411877669141919045780407164332899165726600325498655357752768223849647063310863251366304282738" +
        "675410389244031121303263",
    ]

    # codes_mc contain the 3 sets of the 929 MCs.
    # Each MC is described in the PDF417.TTF font by 3 char. composing 3 time 5 bits. The first bit which is always 1
    # and the last one which is always 0 are into the separator character. 0-2
    codes_mc = [
        "urAxfsypyunkxdwyozpDAulspBkeBApAseAkprAuvsxhypnkutwxgzfDAplsfBkfrApvsuxyfnkptwuwzflspsyfvspxyftwpwzfxyyrxufk" +
        "xFwymzonAudsxEyolkucwdBAoksucidAkokgdAcovkuhwxazdnAotsugydlkoswugjdksosidvkoxwuizdtsowydswowjdxwoyzdwydwjofA" +
        "uFsxCyodkuEwxCjclAocsuEickkocgckcckEcvAohsuayctkogwuajcssogicsgcsacxsoiycwwoijcwicyyoFkuCwxBjcdAoEsuCicckoEg" +
        "uCbcccoEaccEoEDchkoawuDjcgsoaicggoabcgacgDobjcibcFAoCsuBicEkoCguBbcEcoCacEEoCDcECcascagcaacCkuAroBaoBDcCBtfk" +
        "wpwyezmnAtdswoymlktcwwojFBAmksFAkmvkthwwqzFnAmtstgyFlkmswFksFkgFvkmxwtizFtsmwyFswFsiFxwmyzFwyFyzvfAxpsyuyvdk" +
        "xowyujqlAvcsxoiqkkvcgxobqkcvcamfAtFswmyqvAmdktEwwmjqtkvgwxqjhlAEkkmcgtEbhkkqsghkcEvAmhstayhvAEtkmgwtajhtkqww" +
        "vijhssEsghsgExsmiyhxsEwwmijhwwqyjhwiEyyhyyEyjhyjvFkxmwytjqdAvEsxmiqckvEgxmbqccvEaqcEqcCmFktCwwljqhkmEstCigtA" +
        "EckvaitCbgskEccmEagscqgamEDEcCEhkmawtDjgxkEgsmaigwsqiimabgwgEgaEgDEiwmbjgywEiigyiEibgybgzjqFAvCsxliqEkvCgxlb" +
        "qEcvCaqEEvCDqECqEBEFAmCstBighAEEkmCgtBbggkqagvDbggcEEEmCDggEqaDggCEasmDigisEagmDbgigqbbgiaEaDgiDgjigjbqCkvBg" +
        "xkrqCcvBaqCEvBDqCCqCBECkmBgtArgakECcmBagacqDamBDgaEECCgaCECBEDggbggbagbDvAqvAnqBBmAqEBEgDEgDCgDBlfAspsweyldk" +
        "sowClAlcssoiCkklcgCkcCkECvAlhssqyCtklgwsqjCsslgiCsgCsaCxsliyCwwlijCwiCyyCyjtpkwuwyhjndAtoswuincktogwubncctoa" +
        "ncEtoDlFksmwwdjnhklEssmiatACcktqismbaskngglEaascCcEasEChklawsnjaxkCgstrjawsniilabawgCgaawaCiwlbjaywCiiayiCib" +
        "CjjazjvpAxusyxivokxugyxbvocxuavoExuDvoCnFAtmswtirhAnEkxviwtbrgkvqgxvbrgcnEEtmDrgEvqDnEBCFAlCssliahACEklCgslb" +
        "ixAagknagtnbiwkrigvrblCDiwcagEnaDiwECEBCaslDiaisCaglDbiysaignbbiygrjbCaDaiDCbiajiCbbiziajbvmkxtgywrvmcxtavmE" +
        "xtDvmCvmBnCktlgwsrraknCcxtrracvnatlDraEnCCraCnCBraBCCklBgskraakCCclBaiikaacnDalBDiicrbaCCCiiEaaCCCBaaBCDglBr" +
        "abgCDaijgabaCDDijaabDCDrijrvlcxsqvlExsnvlCvlBnBctkqrDcnBEtknrDEvlnrDCnBBrDBCBclAqaDcCBElAnibcaDEnBnibErDnCBB" +
        "ibCaDBibBaDqibqibnxsfvkltkfnAmnAlCAoaBoiDoCAlaBlkpkBdAkosBckkogsebBcckoaBcEkoDBhkkqwsfjBgskqiBggkqbBgaBgDBiw" +
        "krjBiiBibBjjlpAsuswhiloksuglocsualoEsuDloCBFAkmssdiDhABEksvisdbDgklqgsvbDgcBEEkmDDgElqDBEBBaskniDisBagknbDig" +
        "lrbDiaBaDBbiDjiBbbDjbtukwxgyirtucwxatuEwxDtuCtuBlmkstgnqklmcstanqctvastDnqElmCnqClmBnqBBCkklgDakBCcstrbikDac" +
        "lnaklDbicnraBCCbiEDaCBCBDaBBDgklrDbgBDabjgDbaBDDbjaDbDBDrDbrbjrxxcyyqxxEyynxxCxxBttcwwqvvcxxqwwnvvExxnvvCttB" +
        "vvBllcssqnncllEssnrrcnnEttnrrEvvnllBrrCnnBrrBBBckkqDDcBBEkknbbcDDEllnjjcbbEnnnBBBjjErrnDDBjjCBBqDDqBBnbbqDDn" +
        "jjqbbnjjnxwoyyfxwmxwltsowwfvtoxwvvtmtslvtllkossfnlolkmrnonlmlklrnmnllrnlBAokkfDBolkvbDoDBmBAljbobDmDBljbmbDl" +
        "jblDBvjbvxwdvsuvstnkurlurltDAubBujDujDtApAAokkegAocAoEAoCAqsAqgAqaAqDAriArbkukkucshakuEshDkuCkuBAmkkdgBqkkvg" +
        "kdaBqckvaBqEkvDBqCAmBBqBAngkdrBrgkvrBraAnDBrDAnrBrrsxcsxEsxCsxBktclvcsxqsgnlvEsxnlvCktBlvBAlcBncAlEkcnDrcBnE" +
        "AlCDrEBnCAlBDrCBnBAlqBnqAlnDrqBnnDrnwyowymwylswotxowyvtxmswltxlksosgfltoswvnvoltmkslnvmltlnvlAkokcfBloksvDno" +
        "BlmAklbroDnmBllbrmDnlAkvBlvDnvbrvyzeyzdwyexyuwydxytswetwuswdvxutwtvxtkselsuksdntulstrvu",

        "ypkzewxdAyoszeixckyogzebxccyoaxcEyoDxcCxhkyqwzfjutAxgsyqiuskxggyqbuscxgausExgDusCuxkxiwyrjptAuwsxiipskuwgxib" +
        "pscuwapsEuwDpsCpxkuywxjjftApwsuyifskpwguybfscpwafsEpwDfxkpywuzjfwspyifwgpybfwafywpzjfyifybxFAymszdixEkymgzdb" +
        "xEcymaxEEymDxECxEBuhAxasyniugkxagynbugcxaaugExaDugCugBoxAuisxbiowkuigxbbowcuiaowEuiDowCowBdxAoysujidwkoygujb" +
        "dwcoyadwEoyDdwCdysozidygozbdyadyDdzidzbxCkylgzcrxCcylaxCEylDxCCxCBuakxDgylruacxDauaExDDuaCuaBoikubgxDroicuba" +
        "oiEubDoiCoiBcykojgubrcycojacyEojDcyCcyBczgojrczaczDczrxBcykqxBEyknxBCxBBuDcxBquDExBnuDCuDBobcuDqobEuDnobCobB" +
        "cjcobqcjEobncjCcjBcjqcjnxAoykfxAmxAluBoxAvuBmuBloDouBvoDmoDlcbooDvcbmcblxAexAduAuuAtoBuoBtwpAyeszFiwokyegzFb" +
        "wocyeawoEyeDwoCwoBthAwqsyfitgkwqgyfbtgcwqatgEwqDtgCtgBmxAtiswrimwktigwrbmwctiamwEtiDmwCmwBFxAmystjiFwkmygtjb" +
        "FwcmyaFwEmyDFwCFysmziFygmzbFyaFyDFziFzbyukzhghjsyuczhahbwyuEzhDhDyyuCyuBwmkydgzErxqkwmczhrxqcyvaydDxqEwmCxqC" +
        "wmBxqBtakwngydrviktacwnavicxrawnDviEtaCviCtaBviBmiktbgwnrqykmictbaqycvjatbDqyEmiCqyCmiBqyBEykmjgtbrhykEycmja" +
        "hycqzamjDhyEEyChyCEyBEzgmjrhzgEzahzaEzDhzDEzrytczgqgrwytEzgngnyytCglzytBwlcycqxncwlEycnxnEytnxnCwlBxnBtDcwlq" +
        "vbctDEwlnvbExnnvbCtDBvbBmbctDqqjcmbEtDnqjEvbnqjCmbBqjBEjcmbqgzcEjEmbngzEqjngzCEjBgzBEjqgzqEjngznysozgfgfyysm" +
        "gdzyslwkoycfxloysvxlmwklxlltBowkvvDotBmvDmtBlvDlmDotBvqbovDvqbmmDlqblEbomDvgjoEbmgjmEblgjlEbvgjvysegFzysdwke" +
        "xkuwkdxkttAuvButAtvBtmBuqDumBtqDtEDugbuEDtgbtysFwkFxkhtAhvAxmAxqBxwekyFgzCrwecyFaweEyFDweCweBsqkwfgyFrsqcwfa" +
        "sqEwfDsqCsqBliksrgwfrlicsraliEsrDliCliBCykljgsrrCycljaCyEljDCyCCyBCzgljrCzaCzDCzryhczaqarwyhEzananyyhCalzyhB" +
        "wdcyEqwvcwdEyEnwvEyhnwvCwdBwvBsncwdqtrcsnEwdntrEwvntrCsnBtrBlbcsnqnjclbEsnnnjEtrnnjClbBnjBCjclbqazcCjElbnazE" +
        "njnazCCjBazBCjqazqCjnaznzioirsrfyziminwrdzzililyikzygozafafyyxozivivyadzyxmyglitzyxlwcoyEfwtowcmxvoyxvwclxvm" +
        "wtlxvlslowcvtnoslmvrotnmsllvrmtnlvrllDoslvnbolDmrjonbmlDlrjmnblrjlCbolDvajoCbmizoajmCblizmajlizlCbvajvzieifw" +
        "rFzzididyiczygeaFzywuygdihzywtwcewsuwcdxtuwstxttskutlusktvnutltvntlBunDulBtrbunDtrbtCDuabuCDtijuabtijtziFiFy" +
        "iEzygFywhwcFwshxsxskhtkxvlxlAxnBxrDxCBxaDxibxiCzwFcyCqwFEyCnwFCwFBsfcwFqsfEwFnsfCsfBkrcsfqkrEsfnkrCkrBBjckrq" +
        "BjEkrnBjCBjBBjqBjnyaozDfDfyyamDdzyalwEoyCfwhowEmwhmwElwhlsdowEvsvosdmsvmsdlsvlknosdvlroknmlrmknllrlBboknvDjo" +
        "BbmDjmBblDjlBbvDjvzbebfwnpzzbdbdybczyaeDFzyiuyadbhzyitwEewguwEdwxuwgtwxtscustuscttvustttvtklulnukltnrulntnrt" +
        "BDuDbuBDtbjuDbtbjtjfsrpyjdwrozjcyjcjzbFbFyzjhjhybEzjgzyaFyihyyxwEFwghwwxxxxschssxttxvvxkkxllxnnxrrxBBxDDxbbx" +
        "jFwrmzjEyjEjbCzjazjCyjCjjBjwCowCmwClsFowCvsFmsFlkfosFvkfmkflArokfvArmArlArvyDeBpzyDdwCewauwCdwatsEushusEtsht" +
        "kdukvukdtkvtAnuBruAntBrtzDpDpyDozyDFybhwCFwahwixsEhsgxsxxkcxktxlvxAlxBnxDrxbpwnuzboybojDmzbqzjpsruyjowrujjoi" +
        "jobbmyjqybmjjqjjmwrtjjmijmbbljjnjjlijlbjkrsCusCtkFukFtAfuAftwDhsChsaxkExkhxAdxAvxBuzDuyDujbuwnxjbuibubDtjbvj" +
        "jusrxijugrxbjuajuDbtijvibtbjvbjtgrwrjtajtDbsrjtrjsqjsnBxjDxiDxbbxgnyrbxabxDDwrbxrbwqbwn",

        "pjkurwejApbsunyebkpDwulzeDspByeBwzfcfjkprwzfEfbspnyzfCfDwplzzfBfByyrczfqfrwyrEzfnfnyyrCflzyrBxjcyrqxjEyrnxjC" +
        "xjBuzcxjquzExjnuzCuzBpzcuzqpzEuznpzCdjAorsufydbkonwudzdDsolydBwokzdAyzdodrsovyzdmdnwotzzdldlydkzynozdvdvyynm" +
        "dtzynlxboynvxbmxblujoxbvujmujlozoujvozmozlcrkofwuFzcnsodyclwoczckyckjzcucvwohzzctctycszylucxzyltxDuxDtubuubt" +
        "ojuojtcfsoFycdwoEzccyccjzchchycgzykxxBxuDxcFwoCzcEycEjcazcCycCjFjAmrstfyFbkmnwtdzFDsmlyFBwmkzFAyzFoFrsmvyzFm" +
        "FnwmtzzFlFlyFkzyfozFvFvyyfmFtzyflwroyfvwrmwrltjowrvtjmtjlmzotjvmzmmzlqrkvfwxpzhbAqnsvdyhDkqlwvczhBsqkyhAwqkj" +
        "hAiErkmfwtFzhrkEnsmdyhnsqtymczhlwEkyhkyEkjhkjzEuEvwmhzzhuzEthvwEtyzhthtyEszhszyduExzyvuydthxzyvtwnuxruwntxrt" +
        "tbuvjutbtvjtmjumjtgrAqfsvFygnkqdwvEzglsqcygkwqcjgkigkbEfsmFygvsEdwmEzgtwqgzgsyEcjgsjzEhEhyzgxgxyEgzgwzycxytx" +
        "wlxxnxtDxvbxmbxgfkqFwvCzgdsqEygcwqEjgcigcbEFwmCzghwEEyggyEEjggjEazgizgFsqCygEwqCjgEigEbECygayECjgajgCwqBjgCi" +
        "gCbEBjgDjgBigBbCrklfwspzCnsldyClwlczCkyCkjzCuCvwlhzzCtCtyCszyFuCxzyFtwfuwftsrusrtljuljtarAnfstpyankndwtozals" +
        "ncyakwncjakiakbCfslFyavsCdwlEzatwngzasyCcjasjzChChyzaxaxyCgzawzyExyhxwdxwvxsnxtrxlbxrfkvpwxuzinArdsvoyilkrcw" +
        "vojiksrciikgrcbikaafknFwtmzivkadsnEyitsrgynEjiswaciisiacbisbCFwlCzahwCEyixwagyCEjiwyagjiwjCazaiziyzifArFsvmy" +
        "idkrEwvmjicsrEiicgrEbicaicDaFsnCyihsaEwnCjigwrajigiaEbigbCCyaayCCjiiyaajiijiFkrCwvljiEsrCiiEgrCbiEaiEDaCwnBj" +
        "iawaCiiaiaCbiabCBjaDjibjiCsrBiiCgrBbiCaiCDaBiiDiaBbiDbiBgrAriBaiBDaAriBriAqiAnBfskpyBdwkozBcyBcjBhyBgzyCxwFx" +
        "sfxkrxDfklpwsuzDdsloyDcwlojDciDcbBFwkmzDhwBEyDgyBEjDgjBazDizbfAnpstuybdknowtujbcsnoibcgnobbcabcDDFslmybhsDEw" +
        "lmjbgwDEibgiDEbbgbBCyDayBCjbiyDajbijrpkvuwxxjjdArosvuijckrogvubjccroajcEroDjcCbFknmwttjjhkbEsnmijgsrqinmbjgg" +
        "bEajgabEDjgDDCwlljbawDCijiwbaiDCbjiibabjibBBjDDjbbjjjjjFArmsvtijEkrmgvtbjEcrmajEErmDjECjEBbCsnlijasbCgnlbjag" +
        "rnbjaabCDjaDDBibDiDBbjbibDbjbbjCkrlgvsrjCcrlajCErlDjCCjCBbBgnkrjDgbBajDabBDjDDDArbBrjDrjBcrkqjBErknjBCjBBbAq" +
        "jBqbAnjBnjAorkfjAmjAlbAfjAvApwkezAoyAojAqzBpskuyBowkujBoiBobAmyBqyAmjBqjDpkluwsxjDosluiDoglubDoaDoDBmwktjDqw" +
        "BmiDqiBmbDqbAljBnjDrjbpAnustxiboknugtxbbocnuaboEnuDboCboBDmsltibqsDmgltbbqgnvbbqaDmDbqDBliDniBlbbriDnbbrbruk" +
        "vxgxyrrucvxaruEvxDruCruBbmkntgtwrjqkbmcntajqcrvantDjqEbmCjqCbmBjqBDlglsrbngDlajrgbnaDlDjrabnDjrDBkrDlrbnrjrr" +
        "rtcvwqrtEvwnrtCrtBblcnsqjncblEnsnjnErtnjnCblBjnBDkqblqDknjnqblnjnnrsovwfrsmrslbkonsfjlobkmjlmbkljllDkfbkvjlv" +
        "rsersdbkejkubkdjktAeyAejAuwkhjAuiAubAdjAvjBuskxiBugkxbBuaBuDAtiBviAtbBvbDuklxgsyrDuclxaDuElxDDuCDuBBtgkwrDvg" +
        "lxrDvaBtDDvDAsrBtrDvrnxctyqnxEtynnxCnxBDtclwqbvcnxqlwnbvEDtCbvCDtBbvBBsqDtqBsnbvqDtnbvnvyoxzfvymvylnwotyfrxo" +
        "nwmrxmnwlrxlDsolwfbtoDsmjvobtmDsljvmbtljvlBsfDsvbtvjvvvyevydnwerwunwdrwtDsebsuDsdjtubstjttvyFnwFrwhDsFbshjsx" +
        "AhiAhbAxgkirAxaAxDAgrAxrBxckyqBxEkynBxCBxBAwqBxqAwnBxnlyoszflymlylBwokyfDxolyvDxmBwlDxlAwfBwvDxvtzetzdlyenyu" +
        "lydnytBweDwuBwdbxuDwtbxttzFlyFnyhBwFDwhbwxAiqAinAyokjfAymAylAifAyvkzekzdAyeByuAydBytszp",
    ]
    if not string:
        raise ValueError('Received an empty value.')

    def resize(resize_list: list, size: int, save_vals: bool, filler=0):
        """
        VB ReDim analog
        :param resize_list: [[1,2], [5,6]]
        :param size: 4
        :param save_vals: True
        :param filler: 0
        :return: [[1,2,0,0], [5,6,0,0]]
        """
        for inner_list in resize_list:
            orig_size = len(inner_list)
            for num in range(size):
                if len(inner_list) < size:
                    inner_list.append(filler)
                if save_vals:
                    if num > orig_size:
                        inner_list[num] = filler
                else:
                    inner_list[num] = filler

    # Splitting into blocks
    data_list = [[], []]
    list_index = 0

    def get_mode(chain_index_param):
        code_ascii_ = ord(string[chain_index_param - 1: chain_index_param])
        if code_ascii_ in range(48, 57 + 1):
            return 902
        elif code_ascii_ in [9, 10, 13] or code_ascii_ in range(32, 126 + 1):
            return 900
        else:
            return 901

    def get_same_blocks():
        nonlocal chain_index
        nonlocal list_index
        nonlocal data_list
        resize(data_list, list_index + 1, save_vals=True)
        cur_mode = get_mode(chain_index)
        data_list[1][list_index] = cur_mode
        while data_list[1][list_index] == cur_mode:
            data_list[0][list_index] += 1
            chain_index += 1
            if chain_index > len(string):
                break
            cur_mode = get_mode(chain_index)
        list_index += 1

    # Split the string in character blocks of the same type : numeric , text, byte
    # The first column of the array data_list contain the char. number, the second one contain the mode switch
    chain_index = 1
    get_same_blocks()
    while chain_index < len(string) + 1:
        get_same_blocks()

    # We retain "numeric" mode only if it's earning, else "text" mode or even "byte" mode
    # The efficiency limits have been pre-defined according to the previous mode and/or the next mode.
    for i in range(list_index):
        if data_list[1][i] == 902:
            if i == 0:  # It's the first block
                if list_index > 1:  # And there is other blocks behind
                    if data_list[1][i + 1] == 900:
                        # First block and followed by a "text" type block
                        if data_list[0][i] < 8:
                            data_list[1][i] = 900
                    elif data_list[1][i + 1] == 901:
                        # First block and followed by a "byte" type block
                        if data_list[0][i] == 1:
                            data_list[1][i] = 901
            else:
                # It's not the first block
                if i == list_index - 1:
                    # It's the last one
                    if data_list[1][i - 1] == 900:
                        # It's  preceded by a "text" type block
                        if data_list[0][i] < 7:
                            data_list[1][i] = 900
                    elif data_list[1][i - 1] == 901:
                        # It's  preceded by a "byte" type block
                        if data_list[0][i] == 1:
                            data_list[1, i] = 901
                else:
                    # It's not the last block
                    if data_list[1][i - 1] == 901 and data_list[1][i + 1] == 901:
                        # Framed by "byte" type blocks
                        if data_list[0][i] < 4:
                            data_list[1][i] = 901
                    elif data_list[1][i - 1] == 900 and data_list[1][i + 1] == 901:
                        # Preceded by "text" and followed by "byte" (if the reverse it's never interesting to change)
                        if data_list[0][i] < 5:
                            data_list[1][i] = 900
                    elif data_list[1][i - 1] == 900 and data_list[1][i + 1] == 900:
                        # Framed by "text" type blocks
                        if data_list[0][i] < 8:
                            data_list[1][i] = 900

    def regroupe():
        """Bring together same type blocks"""
        nonlocal list_index
        nonlocal data_list
        if list_index > 1:
            i = 1
            while i < list_index:
                if data_list[1][i - 1] == data_list[1][i]:
                    # Bringing together
                    data_list[0][i - 1] = data_list[0][i - 1] + data_list[0][i]
                    j = i + 1
                    # Decrease the list
                    while j < list_index:
                        data_list[0][j - 1] = data_list[0][j]
                        data_list[1][j - 1] = data_list[1][j]
                        j += 1
                    list_index -= 1
                    i -= 1
                i += 1

    # Maintain "text" mode only if it's earning
    regroupe()
    for i in range(list_index):
        if data_list[1][i] == 900 and i > 0:
            # It's not the first (if first, never interesting to change)
            if i == list_index - 1:  # It's the last one
                if data_list[1][i - 1] == 901:
                    # It's  preceded by a "byte" type block
                    if data_list[0][i] == 1:
                        data_list[1][i] = 901
            else:
                # It's not the last one
                if data_list[1][i - 1] == 901 and data_list[1][i + 1] == 901:
                    # Framed by "byte" type blocks
                    if data_list[0][i] < 5:
                        data_list[1][i] = 901
                elif (data_list[1][i - 1] == 901 and data_list[1][i + 1] != 901) or \
                        (data_list[1][i - 1] != 901 and data_list[1][i + 1] == 901):
                    # A "byte" block ahead or behind
                    if data_list[0][i] < 3:
                        data_list[1][i] = 901
    regroupe()

    # Sub routine modulo
    divisor, chain_mult, number = [None] * 3
    chain_mod = ""

    def modulo():
        # chain_mod depict a very large number having more than 9 digits
        # divisor is the divisor, contain the result after return
        # chain_mult contain after return the result of the integer division
        nonlocal chain_mod
        nonlocal divisor
        nonlocal chain_mult
        nonlocal number
        chain_mult = ""
        number = 0
        while chain_mod != "":
            number = number * 10 + int(chain_mod[0])  # Put down a digit
            chain_mod = chain_mod[1:]
            if number < divisor:
                if chain_mult != "":
                    chain_mult += "0"
            else:
                chain_mult += str(int(number // divisor))
            number = number % divisor  # get the remainder
        divisor = number

    # "text" mode processing
    data_list_temp = [[], []]

    # Data compaction
    chain_mc = ''

    # Now we compress datas into the MCs, the MCs are stored in 3 char. in a large string : chain_mc
    chain_index = 1
    for i in range(list_index):
        # Thus 3 compaction modes
        if data_list[1][i] == 900:  # Text
            resize(data_list_temp, int(data_list[0][i]) + 1, save_vals=False)
            # data_list_temp will contain the table number(s) (1 ou several) and the value of each char.
            # Table number encoded in the 4 less weight bits, that is in decimal 1, 2, 4, 8
            for list_index_temp in range(int(data_list[0][i])):
                code_ascii = ord(string[chain_index + list_index_temp - 1: chain_index + list_index_temp])
                if code_ascii == 9:  # HT
                    data_list_temp[0][list_index_temp] = 12
                    data_list_temp[1][list_index_temp] = 12
                elif code_ascii == 10:  # LF
                    data_list_temp[0][list_index_temp] = 8
                    data_list_temp[1][list_index_temp] = 15
                elif code_ascii == 13:  # CR
                    data_list_temp[0][list_index_temp] = 12
                    data_list_temp[1][list_index_temp] = 11
                else:
                    data_list_temp[0][list_index_temp] = \
                        int(ascii_codes[code_ascii * 4 - 127 - 1: code_ascii * 4 - 127 + 1])
                    data_list_temp[1][list_index_temp] = \
                        int(ascii_codes[code_ascii * 4 - 125 - 1: code_ascii * 4 - 125 + 1])

            cur_table = 1  # Default table
            chain_temp = ""
            # Datas are stored in 2 char. in the string TableT
            for j in range(int(data_list[0][i])):
                if (int(data_list_temp[0][j]) & cur_table) > 0:
                    # The char. is in the current table
                    chain_temp += str(data_list_temp[1][j]).zfill(2)
                else:
                    # Obliged to change the table
                    flag = False  # True if we change the table only for 1 char.
                    if j == int(data_list[0][i]) - 1:
                        flag = True
                    else:
                        # No common table with the next char.
                        if (int(data_list_temp[0][j]) & int(data_list_temp[0][j + 1])) == 0:
                            flag = True
                    if flag:
                        # We change only for 1 char., Look for a temporary switch
                        if (int(data_list_temp[0][j]) & 1) > 0 and cur_table == 2:
                            # Table 2 to 1 for 1 char. --> T_UPP
                            chain_temp += "27" + str(data_list_temp[1][j]).zfill(2)
                        elif (int(data_list_temp[0][j]) & 8) > 0:
                            # Table 1 or 2 or 4 to table 8 for 1 char. --> T_PUN
                            chain_temp += "29" + str(data_list_temp[1][j]).zfill(2)
                        else:
                            # No temporary switch available
                            flag = False
                    if not flag:  # We test again flag which is perhaps changed ! Impossible tio use ELSE statement
                        # We must use a bi-state switch
                        # Looking for the new table to use
                        if j == int(data_list[0][i]) - 1:
                            new_table = data_list_temp[0][j]
                        else:
                            new_table = data_list_temp[0][j] if \
                                (int(data_list_temp[0][j]) & int(data_list_temp[0][j + 1])) == 0 else \
                                int(data_list_temp[0][j]) & int(data_list_temp[0][j + 1])
                        # Maintain the first if several tables are possible
                        if new_table in (3, 5, 7, 9, 11, 13, 15):
                            new_table = 1
                        elif new_table in (6, 10, 14):
                            new_table = 2
                        elif new_table == 12:
                            new_table = 4
                        # Select the switch, on occasion we must use 2 switch consecutively
                        if cur_table == 1:
                            if new_table == 2:
                                chain_temp += "27"
                            elif new_table == 4:
                                chain_temp += "28"
                            elif new_table == 8:
                                chain_temp += "2825"
                        elif cur_table == 2:
                            if new_table == 1:
                                chain_temp += "2828"
                            elif new_table == 4:
                                chain_temp += "28"
                            elif new_table == 8:
                                chain_temp += "2825"
                        elif cur_table == 4:
                            if new_table == 1:
                                chain_temp += "28"
                            elif new_table == 2:
                                chain_temp += "27"
                            elif new_table == 8:
                                chain_temp += "25"
                        elif cur_table == 8:
                            if new_table == 1:
                                chain_temp += "29"
                            elif new_table == 2:
                                chain_temp += "2927"
                            elif new_table == 4:
                                chain_temp += "2928"
                        cur_table = new_table
                        chain_temp += str(data_list_temp[1][j]).zfill(2)  # At last we add the char.

            if len(chain_temp) % 4 > 0:
                chain_temp += "29"  # Padding if number of char. is odd
            # Now translate the string chain_temp into CWs
            if i > 0:
                chain_mc += "900"  # Set up the switch except for the first block because "text" is the default
            for j in range(1, len(chain_temp) + 1, 4):
                chain_mc += str(int(int(chain_temp[j - 1:j + 1]) * 30) + int(chain_temp[j + 1: j + 1 + 2])).zfill(3)
        elif data_list[1][i] == 901:  # Octet
            # Select the switch between the 3 possible
            if data_list[0][i] == 1:
                # just 1 byte, thus immediate | 1 seul octet, c'est immidiat
                chain_mc += "913" + str(ord(string[chain_index - 1:chain_index])).zfill(3)
            else:
                # Select the switch for perfect multiple of 6 bytes or no
                if int(data_list[0][i]) % 6 == 0:
                    chain_mc += "924"
                else:
                    chain_mc += "901"
                j = 0
                while j < data_list[0][i]:
                    length = int(data_list[0][i]) - j
                    if length >= 6:
                        # Take groups of 6
                        length = 6
                        total = 0
                        for k in range(length):
                            total += (
                                ord(string[chain_index + j + k - 1: chain_index + j + k]) * 256 ** (length - 1 - k))
                        # at Visual Basic 6 was this strange code:
                        # chain_mod = Format(total, "general number")
                        # I don't know what's this mean...
                        chain_mod = total
                        dummy = ""

                        while True:
                            divisor = 900
                            modulo()
                            dummy = str(divisor).zfill(3) + dummy
                            chain_mod = chain_mult
                            if chain_mult == "":
                                break
                        chain_mc += dummy
                    else:
                        # if it remain a group of less than 6 bytes
                        for k in range(length):
                            chain_mc += str(ord(string[chain_index + j + k - 1: chain_index + j + k])).zfill(3)
                    j += length
        elif data_list[1][i] == 902:  # Numeric
            chain_mc += "902"
            j = 0
            while j < data_list[0][i]:
                length = int(data_list[0][i]) - j
                if length > 44:
                    length = 44
                chain_mod = "1" + string[chain_index + j - 1: chain_index + j - 1 + length]
                dummy = ""
                while True:
                    divisor = 900
                    modulo()
                    dummy = str(divisor).zfill(3) + dummy
                    chain_mod = chain_mult
                    if chain_mult == "":
                        break
                chain_mc += dummy
                j += length
        chain_index += data_list[0][i]

    # chain_mc contain the MC list (on 3 digits) depicting the datas
    # Now we take care of the correction level
    length = len(chain_mc) / 3
    if security < 0:
        # Fixing auto. the correction level according to the standard recommendations
        if length < 41:
            security = 2
        elif length < 161:
            security = 3
        elif length < 321:
            security = 4
        else:
            security = 5
    # Now we take care of the number of CW per row
    length += 1 + (2 ** (security + 1))
    if columns > 30:
        columns = 30
    if columns < 1:
        # With a 3 modules high font, for getting a "square" bar code
        # x = nb. of col. | Width by module = 69 + 17x | Height by module = 3t / x (t is the total number of MCs)
        # Thus we have 69 + 17x = 3t/x <=> 17xІ+69x-3t=0 - Discriminant is 69І-4*17*-3t = 4761+204t
        # thus x=SQR(discr.)-69/2*17
        # 1.3 = balancing factor determined at a guess after tests
        columns = round((math.sqrt(204 * length + 4761) - 69) / (34 / 1.3))
        if columns == 0:
            columns = 1

    # if we go beyong 928 CWs we try to reduce the correction level
    while security > 0:
        # Calculation of the total number of CW with the padding
        length = len(chain_mc) / 3 + 1 + (2 ** (security + 1))
        length = (length // columns + (1 if length % columns > 0 else 0)) * columns
        if length < 929:
            break
        # We must reduce security level
        security -= 1
        Warning('The security level has being lowers not to exceed the 928 CWs. (It\'s not an error, only a warning.)')
    if length > 928:
        raise Exception('string have too many datas, we go beyond the 928 CWs.')
    if length / columns > 90:
        raise Exception('Number of CWs per row too small, we go beyond 90 rows.')
    # Padding calculation
    length = len(chain_mc) / 3 + 1 + (2 ** (security + 1))

    i = 0
    if length // columns < 3:
        i = columns * 3 - length  # A bar code must have at least 3 row
    else:
        if length % columns > 0:
            i = columns - (length % columns)
    # add the padding
    while i > 0:
        chain_mc += "900"
        i -= 1

    # add the length descriptor
    chain_mc = str(int(len(chain_mc) / 3 + 1)).zfill(3) + chain_mc
    # take care of the Reed Solomon codes
    length = int(len(chain_mc) / 3)
    k = 2 ** (security + 1)
    # Reed Solomon codes
    mc_correction = [0, ] * k
    for i in range(int(length)):
        total = (int(chain_mc[i * 3: i * 3 + 3]) + int(mc_correction[k - 1])) % 929
        for j in range(k - 1, -1, -1):
            if j == 0:
                mc_correction[j] = (929 - (total * int(coef_rs[security][j * 3: j * 3 + 3])) % 929) % 929
            else:
                mc_correction[j] = (mc_correction[j - 1] + 929 - (
                    total * int(coef_rs[security][j * 3:j * 3 + 3])) % 929) % 929
    for j in range(k):
        if mc_correction[j] != 0:
            mc_correction[j] = 929 - mc_correction[j]
    # We add theses codes to the string
    for i in range(k - 1, -1, -1):
        chain_mc += str(mc_correction[i]).zfill(3)
    # c1, c2, c3 - Left and right side CWs
    # The CW string is finished
    # Calculation of parameters for the left and right side CWs
    c1 = int((len(chain_mc) / 3 / columns - 1) // 3)
    c2 = int(security * 3 + (len(chain_mc) / 3 / columns - 1) % 3)
    c3 = int(columns - 1)
    # We encode each row
    result = ""
    for i in range(int(len(chain_mc) / 3 / columns)):
        dummy = chain_mc[i * columns * 3: (i * columns * 3) + columns * 3]
        k = int((i // 3) * 30)
        case = i % 3
        if case == 0:
            dummy = str(k + c1).zfill(3) + dummy + str(k + c3).zfill(3)
        elif case == 1:
            dummy = str(k + c2).zfill(3) + dummy + str(k + c1).zfill(3)
        elif case == 2:
            dummy = str(k + c3).zfill(3) + dummy + str(k + c2).zfill(3)
        result += "+*"  # Start with a start char. and a separator
        for j in range(int(len(dummy) / 3)):
            idx = int(int(dummy[j * 3: j * 3 + 3]) * 3)
            result += codes_mc[i % 3][idx: idx + 3] + "*"
        result += "-" + chr(13) + chr(10)  # Add a stop char. and a CRLF
    return result
