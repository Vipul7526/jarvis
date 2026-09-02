#pragma once
#include <string>

namespace jarvis {
struct CapabilityReport { std::string platform; bool local_model_boundary_ready; bool device_control_ready; };
CapabilityReport capability_report();
std::string windows_version_label();
}
