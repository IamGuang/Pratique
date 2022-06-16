<html>
<title>任務一</title>
<script src="https://code.highcharts.com/highcharts.js"></script>
<body>

    <form action="index.php" method="get">
        <span>關鍵字:</span> 
        <input type="text" name="關鍵字">
        <input type="checkbox" name="使用全文檢索[]" value="是" checked>使用全文檢索
        <input type="submit">
    </form>

    <?php

    $servername = "localhost";
    $username = "root"; # thdl
    $password = ""; # thdl
    $dbname = "odsky";
    $conn = new mysqli($servername, $username, $password, $dbname);

    $column_series = array();
    $sql = "";
    $_SESSION['startTime'] = microtime(true);

    if(array_key_exists("關鍵字", $_GET) && $_GET["關鍵字"]!="" && array_key_exists("使用全文檢索", $_GET)){
        $sql = "SELECT 來源系統, COUNT(id) AS 數量 
        FROM `metadata2`
        WHERE MATCH(全文檢索) AGAINST('\"".join(" ", mb_str_split($_GET["關鍵字"]))."\"')
        GROUP BY `來源系統`;";
    }
    else if(array_key_exists("關鍵字", $_GET) && $_GET["關鍵字"]!=""){
        $sql = "SELECT 來源系統, COUNT(id) AS 數量 
        FROM `metadata2`
        WHERE 摘要 like '%".$_GET["關鍵字"]."%' OR 題名 like '%".$_GET["關鍵字"]."%'
        GROUP BY `來源系統`;";
    }
    else{
        $sql = "SELECT 來源系統, COUNT(id) AS 數量 
        FROM `metadata2` 
        GROUP BY `來源系統`;";
    }

    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            array_push($column_series, [
                'name' => $row["來源系統"],
                'data'  => array($row["數量"]),
              ]);
        }
    }

    
    $來源系統西元年數量s = array();
    
    if(array_key_exists("關鍵字", $_GET) && $_GET["關鍵字"]!="" && array_key_exists("使用全文檢索", $_GET)){
        $sql = "SELECT 來源系統, 西元年, COUNT(id) AS 數量 
        FROM `metadata2`
        WHERE MATCH(全文檢索) AGAINST('\"".join(" ", mb_str_split($_GET["關鍵字"]))."\"')
        GROUP BY `西元年`, `來源系統`;";
    }
    else if(array_key_exists("關鍵字", $_GET) && $_GET["關鍵字"]!=""){
        $sql = "SELECT 來源系統, 西元年, COUNT(id) AS 數量 
        FROM `metadata2`
        WHERE 摘要 like '%".$_GET["關鍵字"]."%' OR 題名 like '%".$_GET["關鍵字"]."%'
        GROUP BY `西元年`, `來源系統`;";
    }
    else{
        $sql = "SELECT 來源系統, 西元年, COUNT(id) AS 數量  
        FROM `metadata2` 
        GROUP BY `西元年`, `來源系統`;";
    }
    $result = $conn->query($sql);


    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            array_push($來源系統西元年數量s, [
                '來源系統' => $row["來源系統"],
                '西元年'  => $row["西元年"],
                '數量'  => $row["數量"],
                ]);
        }
    }

    $categories = array();
    for($i=1950 ; $i<2022 ; $i++){
        array_push($categories, $i);
    }

    $來源系統s = ["國史館檔案史料文物查詢系統", "國史館臺灣文獻館典藏管理系統", "臺灣省議會史料總庫", "地方議會議事錄"];
    $來源系統數量s = array();
    foreach($來源系統s as $來源系統){
        $data = array();
        for($i=1950 ; $i<2022 ; $i++){
            $數量 = 0;
            foreach ( $來源系統西元年數量s as $來源系統西元年數量) {
                if ( $i == $來源系統西元年數量["西元年"] &&  $來源系統 == $來源系統西元年數量["來源系統"]) {
                    $數量 = $來源系統西元年數量["數量"];
                    break;
                }
            }
            array_push($data, $數量);
        }
        array_push($來源系統數量s, [
            'name' => $來源系統,
            'data'  => $data,
          ]);
    }

    $conn->close();
    
    echo $sql . "<br>";
    if ($_SESSION['startTime']){ 
        echo "搜尋花了: " . $difference = microtime(true) - $_SESSION['startTime'] . " 毫秒";
    } 
    ?>

<div id="container" style="height: 500px; height:500px;"></div>
<div id="container2" style="height: 500px; height:500px;"></div>
<script>
    Highcharts.chart('container', {
        chart: {
            type: 'column'
        },
        title: {
            text: '<?php if(array_key_exists("關鍵字", $_GET)) echo $_GET["關鍵字"] ?>'
        },
        xAxis: {
            visible: false
        },
        yAxis: {
            min: 0,
            title: {
                text: '件數'
            }
        },
        plotOptions: {
            series:{
                dataLabels:{
                    enabled: true
                }
            },
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: <?php echo json_encode($column_series, JSON_NUMERIC_CHECK, JSON_UNESCAPED_UNICODE) ?>
    });

    Highcharts.chart('container2', {
        chart: {
            type: 'line'
        },
        title: {
            text: '<?php if(array_key_exists("關鍵字", $_GET)) echo $_GET["關鍵字"] ?>'
        },
        xAxis: {
            categories:[<?php echo join(",",$categories) ?>]
        },
        yAxis: {
            min: 0,
            title: {
                text: '件數'
            }
        },
        plotOptions: {
            series:{
                dataLabels:{
                    // enabled: true
                }
            },
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: <?php echo json_encode($來源系統數量s, JSON_NUMERIC_CHECK, JSON_UNESCAPED_UNICODE) ?>
    });
</script>

</body>

</html>
