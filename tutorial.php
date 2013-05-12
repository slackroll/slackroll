<html>
<head>
<title>slackroll: Introduction and Tutorial</title>
<link rel="stylesheet" href="slackroll.css" type="text/css" />
</head>
<body>

<div class="title">slackroll</div>
<div class="subtitle">Introduction and Tutorial</div>
<div class="navbar">Also available: <a href="faq.html">FAQ</a> <a href="slackroll.rss">RSS feed</a></div>

<?php

// A simple example

require_once('classTextile.php');

$textile = new Textile();

$filename = 'tutorial.textile';
$handle = fopen($filename, 'r');
$contents = fread($handle, filesize($filename));
fclose($handle);

echo $textile->TextileThis($contents);

// For untrusted user input, use TextileRestricted instead:
// echo $textile->TextileRestricted($in);


?>

</body>
</html>
