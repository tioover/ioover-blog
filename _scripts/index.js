import Han from 'han-css';
import './smart-underline';

function main() {
  Han(document).initCond()
  .renderElem()
  //.renderHanging()
  //.renderJiya()
  .renderHWS()
  .correctBasicBD()
  .substCombLigaWithPUA();
  
  
  SmartUnderline.init();
}

main();
