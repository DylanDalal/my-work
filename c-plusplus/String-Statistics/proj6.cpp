/* input string
 * string tolower using transform
 * tolower output to string using string constructor
 *
 */
 #include <ctype.h>
 #include <fstream>
 #include <iostream>
 #include <list>
 #include <map>
 #include <string>

 using std::string;
 using std::map;
 using std::cout;
 using std::endl;

string splitter(const string in) {
  string input = in;
  if (isalpha(input.front())) {
    for (auto itr : input) {
      if (isalpha(itr))
        continue;
      else {
        string piece = input.substr(0, input.find(itr));
          std::transform(piece.begin(), piece.end(), piece.begin(), [](unsigned char c)
          { return std::tolower(c); });
        return piece;
      }
    }
  } else if (isdigit(input.front())) {
    for (auto itr : input) {
      if (isdigit(itr))
        continue;
      else
        return input.substr(0, input.find(itr));
    }
  } else {
    for (auto itr : input) {
      if (isdigit(itr))
        return input.substr(0, input.find(itr));
      else if (isalpha(itr))
        return input.substr(0, input.find(itr));
      else
        continue;
    }
  }
  return in;
}

/* I would have much prefered to create separate functions for
 * each of the steps in this process and had a much smaller main.
 * However, I don't exactly know how functions interact with containers
 * when outside of a class; would I have to create global containers?
 * I'll take the time to learn after this assignment. */

int main() {
  bool found = false;
  string in, input, piece;
  int charAr[128], //store characters in array based on ASCII value
  wordCount = 0, numCount = 0, charCount = 0, //totals
  wordMax = 0, numMax = 0, charMax = 0, diffChar = 0, val = 0; //for top 10s
  for (int i = 0; i < 128; i++) //initialize array
    charAr[i] = 0;
  std::list<std::pair<string,int>> numList; //store numbers in list; val, count
  std::list<std::pair<string,int>>::const_iterator counter = numList.begin();
  std::list<std::pair<string,int>> wordList; //store words in list; val, count
  std::list<std::pair<string,int>>::const_iterator counterW = wordList.begin();

  std::list<std::pair<int,int>> charTop;     //
  std::list<std::pair<string,int>> numTop;   // store the most frequent values
  std::list<std::pair<string,int>> wordTop;  //

  std::cout << "Enter input consisting of ASCII characters:" << std::endl;
  in = "start";
  while (!(in.empty())) {
    std::getline(std::cin, in);
    input += in;
  }


  while (!input.empty()) {
    piece = splitter(input);
    /* Count the characters */
    for (auto itr : piece) {
      charAr[int(itr)] += 1;
      charCount++;
    }

    /* Add to the number list */
    if (isdigit(piece.front())) {
      found = false;                              // reset trackers
      counter = numList.begin();

      if (numList.empty())
        numList.push_back(std::make_pair(piece,1));
      else {
        for (auto itr : numList) {                // track iterator value
          if (!(strcmp(itr.first.c_str(), piece.c_str()))) {
            int temp = itr.second;
            temp++;
            std::pair<string,int> replacement = std::make_pair(itr.first,temp);
            numList.insert(counter, replacement); // insert updated count
            numList.erase(counter);               // erase old count
            found = true;
            break;
          }
          counter++;                              // track iterator location
        }
        if (found == false)
          numList.push_back(std::make_pair(piece,1));
      }
    }

    /* Add to the word list */

    else if (isalpha(piece.front())) {
      found = false;                              // reset trackers
      counterW = wordList.begin();

      if (wordList.empty()) {
        wordList.push_back(std::make_pair(piece,1));
      }
      else {
        for (auto itr : wordList) {                 // track iterator value
          if (!(strcmp(itr.first.c_str(), piece.c_str()))) {
            int temp = itr.second;
            temp++;
            std::pair<string,int> replacement = std::make_pair(itr.first,temp);
            wordList.insert(counterW, replacement); // insert updated count
            wordList.erase(counterW);               // erase old count
            found = true;
            break;
          }
          counterW++;                               // track iterator location
        }
        if (found == false) {
          wordList.push_back(std::make_pair(piece,1));
        }
      }
    }
    input.erase(0, piece.size());
  }


  /* Generate top 10 most used characters, numbers and words. */
  wordCount = wordList.size();
  numCount = numList.size();

  if (charCount < 10)                               // Determine if there are
    charMax = charCount;                            // going to be at least 10
  else {                                            // values in the top 10
    for (int i = 0; i < 128; i++) {
      if (charAr[i] != 0)
        diffChar++;
    }
    if (diffChar < 10)
      charMax = diffChar;
    else
      charMax = 10;
  }

  if (wordCount < 10)
    wordMax = wordCount;
  else
    wordMax = 10;

  if (numCount < 10)
    numMax = numCount;
  else
    numMax = 10;

  /* Characters */
  for (int i = 0; i < charMax; i++) {
    std::pair<int,int> top = std::make_pair(0,0); //ascii value, quantity
    for (int o = 0; o < 128; o++) {
      if (charAr[o] > top.second) // if char quantity is greater than top quantity,
        top = std::make_pair(o,charAr[o]);  // overwrite
    } // since i'm iterating by ascending ASCII value i don't need to work ab ==
    charTop.push_back(top);
    charAr[top.first] = 0;
  }

  /* Words */
  for (int i = 0; i < wordMax; i++) {
    std::pair<string,int> top = std::make_pair("empty",0);
    for (auto itr : wordList) {
      if (itr.second > top.second) { // if the count of the word is higher than the top count
        //cout << itr.second << " > " << top.second << endl;
        top = std::make_pair(itr.first, itr.second);
      }
    }
    //cout << "Decided to push pair <" << top.first << "," << top.second << "> to the list." << endl;
    wordList.remove(top);
    wordTop.push_back(top);
  }

  /* Numbers */
  for (int i = 0; i < numMax; i++) {
    std::pair<string,int> top = std::make_pair("0",0);
    for (auto itr : numList) {
      if (itr.second > top.second) // if the count of the word is higher than the top count
        top = std::make_pair(itr.first, itr.second);
    }
    numList.remove(top);
    numTop.push_back(top);
  }

  /* Printing */
  std::cout << "\n\nTotal " << diffChar << " different characters, " << charMax
            << " most used characters:" << std::endl;

  val = 0;
  for (auto itr : charTop) {
    std::cout << "No. " << val << ": " << char(itr.first) << "\t\t" << itr.second << std::endl;
    val++;
  }

  val = 0;
  std::cout << "\n\nTotal " << numCount << " different numbers, " << numMax
            << " most used numbers:" << std::endl;
  for (auto itr : numTop) {
    std::cout << "No. " << val << ": " << itr.first << "\t\t" << itr.second << std::endl;
    val++;
  }

  val = 0;
  std::cout << "\n\nTotal " << wordCount << " different words, " << wordMax
            << " most used words:" << std::endl;
  for (auto itr : wordTop) {
    std::cout << "No. " << val << ": " << itr.first << "\t\t" << itr.second << std::endl;
    val++;
  }
}
