// Orbital Instrument direction: keep the native boundary small, observable, and explicit about unavailable capabilities.
#include <string>
#include <windows.h>

namespace jarvis {

struct CapabilityReport {
  std::string platform;
  bool local_model_boundary_ready;
  bool device_control_ready;
};

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
