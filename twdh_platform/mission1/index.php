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
    $username = "root";
    $password = "";
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
        $sql = "SELECT 來源系統, COUNT(id) AS 數量 FROM `metadata2` GROUP BY `來源系統`;";
    }

    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            array_push($column_series, [
                'name' => $row["來源系統"],
                'data'  => array($row["數量"]),
                'y'  => $row["數量"],
              ]);
        }
    }
    $conn->close();
    
    echo $sql . "<br>";
    if ($_SESSION['startTime']){ 
        echo "搜尋花了: " . $difference = microtime(true) - $_SESSION['startTime'] . " 毫秒";
    } 
    ?>

<div id="container" style="height: 500px; height:500px;"></div>
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
</script>

</body>

</html>