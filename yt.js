const { Module } = require('../main');
const { MODE } = require('../config');
const { skbuffer } = require('raganork-bot');
const axios = require('axios');

const isPrivate = MODE !== 'public';

Module({
  pattern: "sing ?(.*)",
  fromMe: isPrivate,
  use: 'nothing',
  dontAddCommandList: true
}, async (message, match) => {
  const text = match[1];
  const api_url = "https://getsongragnork.serveo.net/audio?url=" + text;

  try {
    const response = await axios.get(api_url);
    const downloadLink = response.data.download_url;

    const audio = await skbuffer(downloadLink);
    await message.client.sendMessage(message.jid, {
      audio,
      mimetype: 'audio/mp4',
      ptt: true // Sends as a push-to-talk audio format
    }, {
      quoted: message.data
    });
  } catch (error) {
    console.error(error);
  }
});
