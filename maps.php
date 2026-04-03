<?php
/**
 * MapIQ — Map listing + texture file listing endpoint
 * Place alongside ut2004-map-viewer.html
 *
 * GET maps.php            → list all maps in Maps/
 * GET maps.php?folder=... → list all texture files in that folder (recursive)
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$baseDir = __DIR__;
$mapsDir = $baseDir . '/Maps';

// ── Texture file listing for a specific map folder ──
if (isset($_GET['folder'])) {
    $rel = trim(str_replace(['..','\\'], ['','/'], $_GET['folder']), '/');
    $dir = $baseDir . '/' . $rel;

    if (!is_dir($dir)) { echo json_encode(['files'=>[]]); exit; }

    $files = [];
    $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir,
        RecursiveDirectoryIterator::SKIP_DOTS));
    foreach ($it as $f) {
        if (preg_match('/\.(dds|tga|png|bmp|jpg|jpeg)$/i', $f->getFilename())) {
            // Return path relative to baseDir (so fetch() can use it directly)
            $abs  = str_replace('\\','/',$f->getRealPath());
            $base = str_replace('\\','/',$baseDir) . '/';
            $files[] = str_replace($base, '', $abs);
        }
    }
    echo json_encode(['files' => $files]);
    exit;
}

// ── Map listing ──
if (!is_dir($mapsDir)) {
    echo json_encode(['error' => 'Maps/ folder not found on server', 'maps' => []]);
    exit;
}

$maps = [];
foreach (scandir($mapsDir) as $entry) {
    if ($entry[0] === '.') continue;
    $mapPath = $mapsDir . '/' . $entry;
    if (!is_dir($mapPath)) continue;

    $objFile = null;
    $texCount = 0;

    foreach (scandir($mapPath) as $file) {
        if (strtolower(substr($file, -4)) === '.obj') $objFile = $file;
    }

    $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($mapPath,
        RecursiveDirectoryIterator::SKIP_DOTS));
    foreach ($it as $f) {
        if (preg_match('/\.(dds|tga|png|bmp|jpg|jpeg)$/i', $f->getFilename())) $texCount++;
    }

    if ($objFile) {
        $maps[] = [
            'name'     => $entry,
            'obj'      => 'Maps/' . $entry . '/' . $objFile,
            'folder'   => 'Maps/' . $entry,
            'textures' => $texCount,
        ];
    }
}

usort($maps, fn($a,$b) => strcmp($a['name'], $b['name']));
echo json_encode(['maps' => $maps]);
