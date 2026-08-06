/**
 * Script to upload audio files to Vercel Blob Storage.
 *
 * Usage:
 *   BLOB_READ_WRITE_TOKEN=xxx npx tsx scripts/upload-audio.ts
 *
 * Requires:
 *   - @vercel/blob installed
 *   - BLOB_READ_WRITE_TOKEN env var (from Vercel dashboard > Settings > Tokens)
 *
 * What it does:
 *   1. Reads all .mp3 files from public/audio/
 *   2. Uploads each to Vercel Blob under the "audio/" prefix
 *   3. Writes data/audio-map.json with { "/audio/file.mp3": "https://blob.vercel-storage.com/..." }
 */

import { put } from "@vercel/blob";
import fs from "fs";
import path from "path";

const AUDIO_DIR = path.resolve(process.cwd(), "public/audio");
const OUTPUT_MAP = path.resolve(process.cwd(), "data/audio-map.json");

async function main() {
  if (!process.env.BLOB_READ_WRITE_TOKEN) {
    console.error("Error: BLOB_READ_WRITE_TOKEN is not set.");
    console.error("Get it from Vercel Dashboard → Settings → Tokens");
    process.exit(1);
  }

  const files = fs.readdirSync(AUDIO_DIR).filter((f) => f.endsWith(".mp3"));

  if (files.length === 0) {
    console.log("No .mp3 files found in public/audio/");
    return;
  }

  console.log(`Found ${files.length} audio files to upload.\n`);

  const map: Record<string, string> = {};

  for (const file of files) {
    const localPath = path.join(AUDIO_DIR, file);
    const blobPath = `audio/${file}`;
    const data = fs.readFileSync(localPath);

    process.stdout.write(`Uploading ${file}... `);

    try {
      const blob = await put(blobPath, data, {
        access: "public",
        contentType: "audio/mpeg",
        addRandomSuffix: false,
      });

      map[`/audio/${file}`] = blob.url;
      console.log(`✓ ${blob.url}`);
    } catch (err: any) {
      console.error(`✗ ${err.message}`);
    }
  }

  fs.mkdirSync(path.dirname(OUTPUT_MAP), { recursive: true });
  fs.writeFileSync(OUTPUT_MAP, JSON.stringify(map, null, 2));

  console.log(`\nDone! Map written to ${OUTPUT_MAP}`);
  console.log(`Total files uploaded: ${Object.keys(map).length}/${files.length}`);
}

main();
