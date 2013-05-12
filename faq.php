<html>
<head>
<title>slackroll: Frequently Asked Questions</title>
<link rel="stylesheet" href="slackroll.css" type="text/css" />
</head>
<body>

<div class="title">slackroll</div>
<div class="subtitle">Frequently Asked Questions</div>
<div class="navbar">Also available: <a href="index.html">Introduction and tutorial</a> <a href="slackroll.rss">RSS feed</a></div>

<?php

// A simple example

require_once('classTextile.php');

$textile = new Textile();

$filename = 'faq.textile';
$handle = fopen($filename, 'r');
$contents = fread($handle, filesize($filename));
fclose($handle);

echo $textile->TextileThis($contents);

// For untrusted user input, use TextileRestricted instead:
// echo $textile->TextileRestricted($in);


?>

</body>
</html>
