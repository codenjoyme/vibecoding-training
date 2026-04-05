package manifest

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
)

type globalManifest struct {
	Skills []string `json:"skills"`
}

type groupManifest struct {
	Skills     []string `json:"skills"`
	SubConfigs []string `json:"sub-configs"`
}

// ResolveSkills loads all relevant manifests for the given groups and returns
// a deduplicated, sorted list of skill directory names to check out.
//
// Resolution order:
//  1. _global.json — skills for everyone (failure is silently skipped)
//  2. Per-group files — <group>.json for each specified group
//  3. Sub-configs referenced by group files — <sub-config>.json
func ResolveSkills(repoPath string, groups []string) ([]string, error) {
	manifestDir := filepath.Join(repoPath, ".manifest")
	skillSet := make(map[string]bool)

	// 1. Load global skills — skip silently if _global.json doesn't exist
	if global, err := loadGlobal(manifestDir); err == nil {
		for _, s := range global.Skills {
			if s != "" {
				skillSet[s] = true
			}
		}
	}

	// 2. Load per-group skills
	for _, group := range groups {
		grp, err := loadGroup(manifestDir, group)
		if err != nil {
			return nil, fmt.Errorf("group %q: %w", group, err)
		}
		for _, s := range grp.Skills {
			if s != "" {
				skillSet[s] = true
			}
		}

		// 3. Load sub-configs referenced by the group
		for _, sub := range grp.SubConfigs {
			subGrp, err := loadGroup(manifestDir, sub)
			if err != nil {
				// Sub-config not found: warn and continue (non-fatal)
				fmt.Printf("Warning: sub-config %q not found, skipping\n", sub)
				continue
			}
			for _, s := range subGrp.Skills {
				if s != "" {
					skillSet[s] = true
				}
			}
		}
	}

	// Convert to sorted slice for deterministic output
	skills := make([]string, 0, len(skillSet))
	for s := range skillSet {
		skills = append(skills, s)
	}
	sort.Strings(skills)
	return skills, nil
}

func loadGlobal(manifestDir string) (*globalManifest, error) {
	path := filepath.Join(manifestDir, "_global.json")
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var m globalManifest
	if err := json.Unmarshal(data, &m); err != nil {
		return nil, fmt.Errorf("invalid _global.json: %w", err)
	}
	return &m, nil
}

func loadGroup(manifestDir, name string) (*groupManifest, error) {
	path := filepath.Join(manifestDir, name+".json")
	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, fmt.Errorf("manifest file not found: %s.json", name)
		}
		return nil, err
	}
	var m groupManifest
	if err := json.Unmarshal(data, &m); err != nil {
		return nil, fmt.Errorf("invalid %s.json: %w", name, err)
	}
	return &m, nil
}
