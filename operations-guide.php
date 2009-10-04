<html>
<head>
<title>slackroll: Operations Guide</title>
<link rel="stylesheet" href="slackroll.css" type="text/css" />
</head>
<body>

<div class="title">slackroll</div>
<div class="subtitle">Operations Guide</div>

<?php

// A simple example

require_once('classTextile.php');

$textile = new Textile();

$filename = 'operations-guide.textile';
$handle = fopen($filename, 'r');
$contents = fread($handle, filesize($filename));
fclose($handle);

echo $textile->TextileThis($contents);

// For untrusted user input, use TextileRestricted instead:
// echo $textile->TextileRestricted($in);


?>

</body>
</html>
