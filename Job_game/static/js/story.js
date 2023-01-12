//要素
var canvas; // canvas要素(HTMLCanvasElement)
var ctx; // 2Dコンテキスト(CanvasRenderingContext2D)
var canvasW = 1049; // canvas要素の横幅(px)
var canvasH = 600; // canvas要素の縦幅(px)
var mouseX; // 最後にクリックされた位置のx座標
var mouseY; // 最後にクリックされた位置のy座標
const back_img = new Image();
const left_img = new Image();
const right_img = new Image();
const msg_img = new Image();
const split = "_,_";
var item ="";
const chapter_fontsize = 40; //チャプター表示の文字サイズ
 let write_count = 0;
 
var chapter_write_end = true; //チャプターの表示が完了したか確認用フラグ
var text_write_end = true; //メッセージの表示が完了したか確認用フラグ
var text_write_delay = 35; //メッセージウインドウの表示スピード（0が速い）
var text_write_fast = false;
var text_write_click = false; //テキスト表示中にクリックされたら即座に全て表示させるフラグ
var write_text; //ページにある本文を読み込む
 

 
//イメージ
const root_ = "images/story_nayami.png";
const msgwin = "images/story_nayami.png";
const suika = "images/story_nayami.png";
const chapter_background = "images/story_back.jpg";
 
//キャラ
const right_b_rina_angry1 = "images/story_rabbit.png";
const right_b_rina_shadow = "images/story_rabbit.png";
 
 
let items = [
    { text: "", back: "", left: "", right: "", msgw: "", chapter: "〜花火の前日〜" },
    { text: "俺の名前は吉野　陸（よしの　りく）北海道へ一人旅に来ている。", back: suika, left: "", right: "", msgw: msgwin, chapter: "" },
    { text: "なのに。", back: suika, left: "", right: "", msgw: msgwin ,chapter: "" },
    { text: "それなのに今は人の畑でスイカの盗み食いをしている。", back: suika, left: "", right: "", msgw: msgwin ,chapter: "" },
    { text: "道具は何もないのでスイカを地面に叩きつけて割れたスイカにかぶりついた。", back: suika, left: "", right: "", msgw: msgwin ,chapter: "" },
    { text: "食べる事に夢中で種ごと飲み込んでいた。", back: suika, left: "", right: "", msgw: msgwin,chapter: "" },
    { text: "？？？：ちょっとアンタなにやってんのよ！", back: suika, left: "", right: right_b_rina_shadow, msgw: msgwin,chapter: "" },
    { text: "背中に投げかけられる声。", back: suika, left: "", right: right_b_rina_shadow, msgw: msgwin, chapter: "" },
    { text: "本当なら驚いて振り向くところだが、そうではなかった。", back: suika, left: "", right: right_b_rina_shadow, msgw: msgwin,chapter: "" },
    { text: "どちらかと言うと寝ている時に誰かに何度も起きろと言われているような・・", back: suika, left: "", right: right_b_rina_shadow, msgw: msgwin,chapter: "" },
    { text: "そう、無視したい感覚だった。", back: suika, left: "", right: right_b_rina_shadow, msgw: msgwin, chapter: "" },
    { text: "？？？：オイ！こらー！", back: suika, left: "", right: right_b_rina_shadow, msgw: msgwin,chapter: "" },
    { text: "？？？：なに勝手に畑入ってスイカ食ってんのよ！", back: suika, left: "", right: right_b_rina_shadow, msgw: msgwin,chapter: "" },
    { text: "何回目の呼びかけだろうか、ようやく正気に戻り振り向くべき状況であると認識してゆっくり振り向く。", back: suika, left: "", right: right_b_rina_shadow,chapter: "" },
    { text: "陸：（女の子だ。高校生？）", back: suika, left: "", right: right_b_rina_angry1, msgw: msgwin,chapter: "" },
    { text: "女の子：何やってんのかって聞いてんの！ドロボー？", back: suika, left: "", right: right_b_rina_angry1, msgw: msgwin ,chapter: "" },
    { text: "", back: "", left: "", right: "", msgw: "", chapter: "終わりです。クリックでスタートに戻ります。" },
];
var items_number = 0;
 
 
canvas = document.getElementById('axisCanvas');
  // canvas要素を取得し、サイズ設定
   
  canvas.width = canvasW;
  canvas.height = canvasH;
 
  // 描画のために2Dコンテキスト取得
  ctx = canvas.getContext('2d');
 
function chapter_wiew(chapter){
    //黒背景で文字を黒から白に変更
    var count = 0;//アニメーションカウンター
    var timer = setInterval(function(){
        text_write_end = false;
        ctx.font = "bold " + chapter_fontsize + "px 'ＭＳ ゴシック'";
        ctx.fillStyle= "rgb( " + (255/20) * count + ", " + (255/20) * count + ", " + (255/20) * count + " )"
        back_img.src = chapter_background;
        ctx.drawImage(back_img, 0, 0, 1049, 600); //背景描写
        ctx.fillText(chapter, canvasW / 2 - chapter.length * chapter_fontsize / 2 , canvasH / 2 - 40, canvasW); //文章
        count++;
        if(count>20){
            text_write_end = true;
            clearInterval(timer);
        }
    },100);
};
//文字を表示する際の１文字ずつ判定
    // setIntervalの基本
    max_row = 28;
    var timer1 = null;
    var cnt = 0;
 
    function event() {
        chapter_write_end = false;
        write_text.length;
        row = 0;
        if (cnt > max_row * 1)row = 1;
        if (cnt > max_row * 2)row = 2;
        if (cnt > max_row * 3)row = 3;
        column = 0;
        if (cnt > max_row * 1)column = -1 * max_row - 1;
        if (cnt > max_row * 2)column = -2 * max_row - 1;
        if (cnt > max_row * 3)column = -3 * max_row - 1;
        ctx.fillText(write_text.charAt(cnt), 70 + cnt * 30 + column * 30, 480+ row * 30, 900); //文章
        cnt++;
        //文字描写中にクリックされた場合は一気に描写する
        if (text_write_fast == true){
            row = 0;
            column = 0;
            cnt = 0;
            clearInterval(timer1);
            text_write_fast = false;
            timer1 = setInterval(event, 1);
        }
        if (cnt >= write_text.length && timer1 != null) {
            // 文字数以上になったら、タイマーを停止する
            chapter_write_end = true;
            text_write_click = false;
            row = 0;
            column = 0;
            cnt = 0;
            clearInterval(timer1);
        }
    }
function next_item(){
    const chapter = (String(items[items_number].chapter)); //チャプター文字取得
    write_text = (String(items[items_number].text)); //文章を
    // 一度描画をクリア
    ctx.clearRect(0, 0, canvasW, canvasH);
    ctx.fillStyle = 'white';
    ctx.font = "30px 'ＭＳ ゴシック'";
    ctx.textAlign = "left";
    ctx.textBaseline = "top";
    left_img.src = "";
    left_img.src = String(items[items_number].left);
 
    write_flag = "NG";
    right_img.src = "";
    right_img.src = String(items[items_number].right);
 
    msg_img.src = "";
    msg_img.src = String(items[items_number].msgw);
 
    back_img.src = "";  // 一度か空にしないと同じ画像がonloadで読み込まれないので回避策として入れる
    back_img.src = String(items[items_number].back);  // 画像のURLを指定
 
    back_img.onload = () => {
        ctx.drawImage(back_img, 0, 0, 1049, 600); //背景描写
        ctx.drawImage(left_img, 50, 50); //left
        ctx.drawImage(right_img, 600, 50); //
        ctx.drawImage(msg_img, 0, 450, 1049, 150); //メッセージウィンドウ
        timer1 = setInterval(event, text_write_delay);
    };
    //読み込みページにチャプター文字がある場合はチャプターモードで表示する
    if ( chapter != "" ){
        chapter_wiew(chapter);
    }
};
function keydownfunc( event ) {
    //押されたボタンに割り当てられた数値（すうち）を、key_codeに代入
    var key_code = event.keyCode;
    if( key_code === 37 ) ;     //「左ボタン」が押されたとき
    if( key_code === 38 ) ;     //「上ボタン」が押されたとき
    if( key_code === 39 ) next();       //「右ボタン」が押されたとき
    if( key_code === 40 ) next();       //「下ボタン」が押されたとき
}
function next(){
    //クリックされた場合に前の読み込みが完了していれば次のページへ。
    //そうでなければ読み込みスピードをMAXにする。
    if ( chapter_write_end == true && text_write_end == true ){
        next_item();
        items_number++;
    }else{
        if ( text_write_click == false ){
            text_write_fast = true;
            text_write_click = true;
        }
    }
    if(items.length <= items_number) items_number = 0; //終わったら最初に戻る
}
window.onload = function() {
  next_item();
  items_number++;
  canvas.onclick = function(e) {
      var rect = e.target.getBoundingClientRect();
      mouseX = e.clientX - Math.floor(rect.left) - 2;
      mouseY = e.clientY - Math.floor(rect.top) - 2;
      console.log(mouseX,mouseY);
      next();
  }
};
addEventListener( "keydown", keydownfunc );