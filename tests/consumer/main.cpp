#include <RTMA.h>

int main() {
  CMessage message;
  return message.IsDynamic() ? 1 : 0;
}
