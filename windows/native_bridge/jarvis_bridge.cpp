// Orbital Instrument direction: keep the native boundary small, observable, and explicit about unavailable capabilities.
#include "jarvis_bridge.h"
#if defined(_WIN32)
#include <windows.h>
#endif

namespace jarvis {

CapabilityReport capability_report() {
  return {
      "windows",
      false, // Set true only after a real llama.cpp/GGUF health check succeeds.
      false  // Set true only after a paired device has an authorized route.
  };
}

std::string windows_version_label() {
  return "Windows native bridge / Win32 boundary";
}

}  // namespace jarvis
