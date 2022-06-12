<?php
header("Content-Type:text/html; charset=utf-8");
set_time_limit(30000000000000);

// $sql = "SELECT id, `摘要`, `題名` FROM `metadata2` WHERE 全文檢索=''";
// $result = $conn->query($sql);
// if ($result->num_rows > 0) {
//     while ($row = $result->fetch_assoc()) {
//       $split = $mysqli->real_escape_string(join(" ", mb_str_split($row["題名"])) . " " . join(" ",mb_str_split($row["摘要"])));
//       $query = "UPDATE metadata2 SET 全文檢索 = '". $split ."' WHERE id = " . $row["id"];
//       $conn->query($query);
//     }
// }
// $conn->close();

// $sql = "SELECT * FROM `metadata` WHERE 1";
// $sql = "DELETE FROM `metadata` WHERE 1";
// $conn->query($sql);
// id / OD 唯一編碼 來源系統縮寫_系統原典藏號
// 來源系統 
// 來源系統縮寫 系統縮寫
// 文件原系統頁面URL 
// [有沒有被匯入詳細資料]  是否
// [original] 將由CSV及爬蟲來的最詳細的資料存為json檔
// 題名 由摘要擷取第一個標點前的句子
// 摘要
// 類目階層
// 原始時間記錄
// 西元年 yyyy 由起始日期中截取西元年
// 起始時間 yyyymmdd
// 結束時間 yyyymmdd
// 相關人員 多值以";"半型分號區隔
// 相關地點
// 相關組織
// 關鍵詞

function 清整日期(string $l)
{
   return str_replace('/00', '/01', $l);
}

function 刪除前後($data)
{
   $num = count($data);
   for ($c = 0; $c < $num; $c++) {
      $data[$c] = substr($data[$c], 2, strlen($data[$c]) - 2);
      $data[$c] = substr($data[$c], 0, strlen($data[$c]) - 1);
   }
   return $data;
}

function 插入資料($來源系統, $來源系統縮寫, $題名, $摘要, $類目階層, $原始時間記錄, $西元年, $起始時間, $結束時間, $典藏號, $相關人員, $相關地點, $相關組織, $文件原系統頁面URL)
{
   $servername = "localhost";
   $username = "root";
   $password = "";
   $dbname = "odsky";
   $conn = new mysqli($servername, $username, $password, $dbname);

   $sql = "INSERT INTO `metadata2` (
      `來源系統`, 
      `來源系統縮寫`, 
      `題名`, 
      `摘要`, 
      `類目階層`, 
      `原始時間記錄`, 
      `西元年`, 
      `起始時間`, 
      `結束時間`, 
      `典藏號`, 
      `相關人員`, 
      `相關地點`, 
      `相關組織`, 
      `文件原系統頁面URL`,
      `全文檢索`,
      `有沒有被匯入詳細資料`
      )
            VALUES (
               '" . $來源系統 . "', 
               '" . $來源系統縮寫 . "',
               '" . $conn->real_escape_string($題名) . "',
               '" . $conn->real_escape_string($摘要) . "',
               '" . str_replace("/", ";", $類目階層) . "',
               '" . $原始時間記錄 . "',
               '" . $西元年 . "',
               '" . $起始時間 . "',
               '" . $結束時間 . "',
               '" . $典藏號 . "',
               '" . str_replace("，", ";", $相關人員) . "',
               '" . str_replace("，", ";", $相關地點) . "',
               '" . str_replace("，", ";", $相關組織) . "',
               '" . $文件原系統頁面URL . "',
               '" . $conn->real_escape_string(join(" ", mb_str_split($題名)) . " " . join(" ", mb_str_split($摘要))) . "',
               0
               );
            ";
   $conn->query($sql);
   $conn->close();
}

// SELECT 來源系統, count(*) FROM `metadata2` GROUP by 來源系統;

$path = "./csvs/";

foreach (scandir($path) as  $file) {
   $row = 1;
   if ($file != "." && $file != ".." && ($handle = fopen($path . $file, "r")) !== FALSE) {
      try {
         while (($data = fgetcsv($handle, 1000000, ",", '"')) !== FALSE) {
            if (str_starts_with($file, "NDAP") && $row > 4 && count($data) == 6) {
               // 'no' '="資料集"' '="典藏號"' '="瀏覽階層"' '="日期描述"' '="內容摘要"'
               $data = 刪除前後($data);
               //   "文件時間(time_varchar)": [ a.split('~')[0].replace("-","/").replace(" ","") if len(a.split('~'))==2 else "00000000" for a in csv_df['"日期描述"']] ,
               if (str_contains($data[4], "~"))
                  插入資料("臺灣省議會史料總庫", "NDAP",  explode("，", $data[5])[0], $data[5], $data[3], $data[4], substr($data[4], 0, 4), explode("~", $data[4])[0], explode("~", $data[4])[1], $data[2], NULL, NULL, NULL, NULL);
               else
                  插入資料("臺灣省議會史料總庫", "NDAP",  explode("，", $data[5])[0], $data[5], $data[3], $data[4], "0000", "", "", $data[2], NULL, NULL, NULL, NULL);
            } else if (str_starts_with($file, "AHCMS")  && $row > 4 && count($data) == 8) {
               // "no","入藏登錄號","卷名","檔案系列","題名摘要","卷件開始日期","卷件結束日期","數位典藏號"
               插入資料("國史館檔案史料文物查詢系統", "AHCMS", $data[2], $data[4], $data[3], $data[5] . '-' . $data[6], substr($data[5], 0, 4), 清整日期($data[5]), 清整日期($data[6]), $data[7], NULL, NULL, NULL, NULL);
            } else if (str_starts_with($file, "AHTWH")  && $row > 4 && count($data) == 7) {
               // 'no' '="data_type"' '="數位典藏號"' '="title"' '="檔案系列"' '="date_from"''="date_stop"'
               $data = 刪除前後($data);
               插入資料("國史館臺灣文獻館典藏管理系統", "AHTWH", explode("，", $data[3])[0], $data[3], $data[4], $data[5] . '-' . $data[6], substr($data[5], 0, 4), 清整日期($data[5]), 清整日期($data[6]), $data[2], NULL, NULL, NULL, NULL);
            } else if ((str_starts_with($file, "tlcda") or str_contains($file, "#meeting")) && $row > 5 && count($data) == 27) {
               // "","書目序號","議會名稱","資料類型","書目名稱","典藏序號","類別階層","會議階層","內容類別","頁次起","頁次迄","影像序起","影像序迄","日期起","日期迄","內容摘要","會議主席","提案議員","相關議員","請願人","機關","相關機關","請願機關","文號","參照","","資料連結"
               插入資料("地方議會議事錄", "TLCDA", $data[4], $data[15], $data[7], $data[13] . '-' . $data[14], substr($data[13], 0, 4), 清整日期($data[13]), 清整日期($data[14]), $data[5], $data[16] . "，" . $data[17] . "，" . $data[18] . "，" . $data[19], NULL, $data[20] . "，" . $data[21] . "，" . $data[22], $data[26]);
            }
            $row++;
         }
         echo $file . "成功 <br>";
         rename($path . $file, "./dones/" . $file, null);
      } catch (Exception $ex) {
         echo $file . "失敗 <br>";
         rename($path . $file, "./errors/" . $file, null);
      }
      fclose($handle);
   }
}

echo "完成";
