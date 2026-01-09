#pragma once

#if defined _WIN32
#if defined TETHER_SUM_EXPORTS
#define TETHER_SUM_API __declspec(dllexport)
#elif defined TETHER_SUM_IMPORTS
#define TETHER_SUM_API __declspec(dllimport)
#else
#define TETHER_SUM_API
#endif
#else
#define TETHER_SUM_API __attribute__((visibility("default")))
#endif